"""
srttotxt.py — Convert .srt/.vtt files or YouTube URLs to clean .txt
Dependencies: pip install webvtt-py yt-dlp typer
"""

from __future__ import annotations

import re
import json
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Iterable

import typer

import webvtt
import yt_dlp

# Initialize Typer app
app = typer.Typer(help="Convert .srt/.vtt files or YouTube URLs to clean .txt")

# ── Config ────────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path(r"C:\Subtitles")
LOG_DIR    = OUTPUT_DIR / "logs"
TMP_DIR    = OUTPUT_DIR / "_tmp"

RETRY_ATTEMPTS   = 3
RETRY_BASE_DELAY = 2   # seconds, doubles each attempt

# Lines to strip from captions (music, sound effects, etc.)
NOISE_PATTERNS = re.compile(
    r'^\s*(\[.*?\]|\(.*?\)|♪.*?♪|♪|&nbsp;|<[^>]+>)\s*$',
    re.IGNORECASE
)

# ── Logging ───────────────────────────────────────────────────────────────────
def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"

    logger = logging.getLogger("srttotxt")
    logger.setLevel(logging.DEBUG)

    # File handler — full detail
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))

    # Console handler — clean output
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(message)s'))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# ── Lazy logger — initialised on first use inside main() ─────────────────────
log: logging.Logger | None = None

def get_log() -> logging.Logger:
    global log
    if log is None:
        log = setup_logger()
    return log

# ── Text cleaning ─────────────────────────────────────────────────────────────
def clean_text(captions: Iterable[webvtt.Caption], paragraph: bool = False) -> str:
    lines = []
    for caption in captions:
        for line in caption.text.strip().splitlines():
            line = re.sub(r'<[^>]+>', '', line).strip()   # strip residual tags
            if not line:
                continue
            if NOISE_PATTERNS.match(line):
                continue
            if lines and line == lines[-1]:                # dedupe consecutive
                continue
            lines.append(line)

    if not lines:
        return ""

    if paragraph:
        return ' '.join(lines) + '\n'
    return '\n'.join(lines) + '\n'

def is_output_valid(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0

# ── Metadata helpers ──────────────────────────────────────────────────────────
def build_metadata(info: dict) -> dict:
    return {
        "title":      info.get("title", ""),
        "channel":    info.get("channel") or info.get("uploader", ""),
        "url":        info.get("webpage_url", ""),
        "date":       info.get("upload_date", ""),      # YYYYMMDD string, e.g. "20240115"
        "duration":   info.get("duration_string") or str(info.get("duration", "")),
        "converted_at": datetime.now().isoformat(timespec='seconds'),
    }

def write_metadata(meta: dict, stem_path: Path):
    """Write both a .json sidecar and prepend a header block to the .txt."""
    logger = get_log()

    # JSON sidecar
    json_path = stem_path.with_suffix('.json')
    json_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    logger.debug(f"Metadata JSON -> {json_path}")

    # Prepend header to the existing .txt (guard against double-prepend)
    txt_path = stem_path.with_suffix('.txt')
    if txt_path.exists():
        original = txt_path.read_text(encoding='utf-8')
        if not original.startswith('# '):
            header = (
                f"# {meta['title']}\n"
                f"Channel  : {meta['channel']}\n"
                f"URL      : {meta['url']}\n"
                f"Date     : {meta['date']}\n"
                f"Duration : {meta['duration']}\n"
                f"Converted: {meta['converted_at']}\n"
                f"{'─' * 60}\n\n"
            )
            txt_path.write_text(header + original, encoding='utf-8')

# ── Local file conversion ─────────────────────────────────────────────────────
def convert_file(input_path: Path, paragraph: bool = False):
    logger = get_log()
    ext = input_path.suffix.lower()

    if ext == '.vtt':
        captions = webvtt.read(str(input_path))
    elif ext == '.srt':
        captions = webvtt.from_srt(str(input_path))
    else:
        raise ValueError(f"Unsupported format: {ext}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / input_path.with_suffix('.txt').name
    text = clean_text(captions, paragraph)

    if not text.strip():
        raise ValueError("Output is empty after cleaning — source may have no readable captions.")

    out.write_text(text, encoding='utf-8')

    if not is_output_valid(out):
        raise IOError(f"Output file missing or empty: {out}")

    logger.info(f"  [OK]   {input_path.name} -> {out.name}")

# ── YouTube conversion ────────────────────────────────────────────────────────
def _sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()

def _ytdlp_opts(lang: str, use_cookies: bool) -> dict:
    opts = {
        'skip_download':     True,
        'writesubtitles':    True,        # manual subs first
        'writeautomaticsub': True,        # fallback to auto
        'subtitleslangs':    [lang, f'{lang}-orig'],
        'subtitlesformat':   'vtt',
        'outtmpl':           str(TMP_DIR / '%(title)s.%(ext)s'),
        'quiet':             True,
        'no_warnings':       True,
        'postprocessors': [{
            'key':    'FFmpegSubtitlesConvertor',
            'format': 'vtt',
        }],
    }
    if use_cookies:
        opts['cookiesfrombrowser'] = ('chrome',)
    return opts

def convert_url(url: str, lang: str = 'en', paragraph: bool = False, use_cookies: bool = False):
    logger = get_log()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    info = None
    last_error = None

    # ── Retry loop ────────────────────────────────────────────────────────────
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            logger.debug(f"Attempt {attempt}/{RETRY_ATTEMPTS}: {url}")
            with yt_dlp.YoutubeDL(_ytdlp_opts(lang, use_cookies)) as ydl:
                info = ydl.extract_info(url, download=True)
            break
        except Exception as e:
            last_error = e
            logger.warning(f"  [RETRY {attempt}/{RETRY_ATTEMPTS}] {e}")
            if attempt < RETRY_ATTEMPTS:
                time.sleep(RETRY_BASE_DELAY ** attempt)
    else:
        raise ConnectionError(f"All {RETRY_ATTEMPTS} attempts failed: {last_error}")

    title    = info.get('title', 'output')
    safe     = _sanitize(title)

    # ── Find downloaded VTT ───────────────────────────────────────────────────
    vtt_files = list(TMP_DIR.glob('*.vtt'))
    if not vtt_files:
        raise FileNotFoundError(
            f"No subtitles found for lang='{lang}'. "
            "The video may lack captions in that language."
        )

    # Prefer manual over auto: yt-dlp marks auto-generated as .en-orig.vtt
    def sub_priority(p: Path) -> int:
        return 1 if re.search(r'\.(auto|orig)\.vtt$', p.name.lower()) else 0

    vtt_files.sort(key=sub_priority)
    vtt = vtt_files[0]

    # ── Convert ───────────────────────────────────────────────────────────────
    captions = webvtt.read(str(vtt))
    text     = clean_text(captions, paragraph)

    if not text.strip():
        raise ValueError("Output is empty after cleaning — captions may be noise-only.")

    out = OUTPUT_DIR / f"{safe}.txt"
    out.write_text(text, encoding='utf-8')

    if not is_output_valid(out):
        raise IOError(f"Output file missing or empty: {out}")

    # ── Metadata ──────────────────────────────────────────────────────────────
    meta = build_metadata(info)
    write_metadata(meta, OUTPUT_DIR / safe)

    logger.info(f"  [OK]   \"{title}\"")
    logger.info(f"         -> {out}")
    logger.debug(f"Metadata: {json.dumps(meta)}")

    # ── Cleanup tmp ───────────────────────────────────────────────────────────
    for f in TMP_DIR.glob('*'):
        try:
            f.unlink()
        except Exception:
            pass
    try:
        TMP_DIR.rmdir()
    except Exception:
        pass

# ── Batch processing ──────────────────────────────────────────────────────────
def process_batch(batch_file: Path, lang: str, paragraph: bool, use_cookies: bool):
    logger = get_log()
    urls = [
        line.strip()
        for line in batch_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')
    ]

    if not urls:
        logger.info("Batch file is empty.")
        return

    logger.info(f"Batch: {len(urls)} URLs from {batch_file.name}\n")
    ok, fail = 0, 0

    for i, url in enumerate(urls, 1):
        logger.info(f"[{i}/{len(urls)}] {url}")
        try:
            convert_url(url, lang, paragraph, use_cookies)
            ok += 1
        except Exception as e:
            logger.error(f"  [FAIL] {e}")
            fail += 1

    logger.info(f"\nBatch done: {ok} OK, {fail} failed.")

# ── Entry point ───────────────────────────────────────────────────────────────
@app.command()
def main(
    target: str = typer.Argument(
        ..., 
        help="Target URL, local file (.srt/.vtt), folder, or batch .txt file"
    ),
    lang: str = typer.Option(
        "en", 
        "--lang",
        help="Language code for yt-dlp subtitles"
    ),
    paragraph: bool = typer.Option(
        False, 
        "--paragraph", 
        help="Format output as a single paragraph"
    ),
    cookies: bool = typer.Option(
        False, 
        "--cookies", 
        help="Use Chrome browser cookies for YouTube"
    ),
    open_output: bool = typer.Option(
        False, 
        "--open", 
        help="Open output folder when done"
    ),
    batch: bool = typer.Option(
        False, 
        "--batch", 
        help="Treat target as a batch .txt file of URLs"
    )
):
    """
    srttotxt: Convert .srt/.vtt files or YouTube URLs to clean .txt
    """
    logger = get_log()

    if not target:
        logger.error("No target specified.")
        raise typer.Exit(code=1)

    ok, fail = 0, 0

    # ── Batch mode ────────────────────────────────────────────────────────────
    if batch:
        bf = Path(target)
        if not bf.is_file():
            logger.error(f"Batch file not found: {bf}")
            raise typer.Exit(code=1)
        process_batch(bf, lang, paragraph, cookies)

    # ── URL ───────────────────────────────────────────────────────────────────
    elif target.startswith('http://') or target.startswith('https://'):
        try:
            convert_url(target, lang, paragraph, cookies)
            ok += 1
        except Exception as e:
            logger.error(f"  [FAIL] {e}")
            fail += 1
        logger.info(f"\nDone: {ok} converted, {fail} failed.")

    # ── File / folder ─────────────────────────────────────────────────────────
    else:
        path = Path(target)
        if path.is_dir():
            files = list(path.glob('*.srt')) + list(path.glob('*.vtt'))
            if not files:
                logger.info(f"No .srt/.vtt files found in: {path}")
                raise typer.Exit(code=0)
        elif path.is_file():
            files = [path]
        else:
            logger.error(f"Path not found: {target}")
            raise typer.Exit(code=1)

        for f in files:
            try:
                convert_file(f, paragraph)
                ok += 1
            except Exception as e:
                logger.error(f"  [FAIL] {f.name}: {e}")
                fail += 1

        logger.info(f"\nDone: {ok} converted, {fail} failed.")

    # ── Open output folder ────────────────────────────────────────────────────
    if open_output:
        subprocess.Popen(['explorer', str(OUTPUT_DIR)])

if __name__ == '__main__':
    app()