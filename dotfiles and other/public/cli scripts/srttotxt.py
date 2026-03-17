"""
srttotxt.py — Convert .srt/.vtt files or YouTube URLs to clean .txt
Dependencies: pip install webvtt-py yt-dlp
"""

import sys
import re
import json
import time
import logging
from pathlib import Path
from datetime import datetime

import webvtt
import yt_dlp

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


log = setup_logger()


# ── Text cleaning ─────────────────────────────────────────────────────────────
def clean_text(captions, paragraph: bool = False) -> str:
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
        "title":    info.get("title", ""),
        "channel":  info.get("channel") or info.get("uploader", ""),
        "url":      info.get("webpage_url", ""),
        "date":     info.get("upload_date", ""),      # YYYYMMDD
        "duration": info.get("duration_string") or str(info.get("duration", "")),
        "converted_at": datetime.now().isoformat(timespec='seconds'),
    }


def write_metadata(meta: dict, stem_path: Path):
    """Write both a .json sidecar and prepend a header block to the .txt."""

    # JSON sidecar
    json_path = stem_path.with_suffix('.json')
    json_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    log.debug(f"Metadata JSON -> {json_path}")

    # Prepend header to the existing .txt
    txt_path = stem_path.with_suffix('.txt')
    if txt_path.exists():
        original = txt_path.read_text(encoding='utf-8')
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

    log.info(f"  [OK]   {input_path.name} -> {out.name}")


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


def convert_url(url: str, lang: str = 'en', paragraph: bool = False,
                use_cookies: bool = False):

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    info = None
    last_error = None

    # ── Retry loop ────────────────────────────────────────────────────────────
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            log.debug(f"Attempt {attempt}/{RETRY_ATTEMPTS}: {url}")
            with yt_dlp.YoutubeDL(_ytdlp_opts(lang, use_cookies)) as ydl:
                info = ydl.extract_info(url, download=True)
            break
        except Exception as e:
            last_error = e
            log.warning(f"  [RETRY {attempt}/{RETRY_ATTEMPTS}] {e}")
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

    # Prefer manual over auto: yt-dlp marks auto as .<lang>-orig. or .auto.
    def sub_priority(p: Path):
        name = p.name.lower()
        if 'orig' in name or 'auto' in name:
            return 1
        return 0

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

    log.info(f"  [OK]   \"{title}\"")
    log.info(f"         -> {out}")
    log.debug(f"Metadata: {json.dumps(meta)}")

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
    urls = [
        line.strip()
        for line in batch_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')
    ]

    if not urls:
        log.info("Batch file is empty.")
        return

    log.info(f"Batch: {len(urls)} URLs from {batch_file.name}\n")
    ok, fail = 0, 0

    for i, url in enumerate(urls, 1):
        log.info(f"[{i}/{len(urls)}] {url}")
        try:
            convert_url(url, lang, paragraph, use_cookies)
            ok += 1
        except Exception as e:
            log.error(f"  [FAIL] {e}")
            fail += 1

    log.info(f"\nBatch done: {ok} OK, {fail} failed.")


# ── Entry point ───────────────────────────────────────────────────────────────
def parse_args(argv: list) -> dict:
    args = {
        'target':      None,
        'lang':        'en',
        'paragraph':   False,
        'cookies':     False,
        'open_output': False,
        'batch':       False,
    }

    i = 1
    while i < len(argv):
        a = argv[i]
        if a == '-lang' and i + 1 < len(argv):
            args['lang'] = argv[i + 1]; i += 2
        elif a == '-paragraph':
            args['paragraph'] = True; i += 1
        elif a == '-cookies':
            args['cookies'] = True; i += 1
        elif a == '-open':
            args['open_output'] = True; i += 1
        elif a == '-batch':
            args['batch'] = True; i += 1
        else:
            args['target'] = a; i += 1

    return args


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  srttotxt.py <url>              [-lang fr] [-paragraph] [-cookies] [-open]\n"
            "  srttotxt.py <file|folder>      [-paragraph] [-open]\n"
            "  srttotxt.py <urls.txt> -batch  [-lang fr] [-paragraph] [-cookies] [-open]\n"
        )
        sys.exit(1)

    a = parse_args(sys.argv)

    if not a['target']:
        log.error("No target specified.")
        sys.exit(1)

    target = a['target']
    ok, fail = 0, 0

    # ── Batch mode ────────────────────────────────────────────────────────────
    if a['batch']:
        bf = Path(target)
        if not bf.is_file():
            log.error(f"Batch file not found: {bf}")
            sys.exit(1)
        process_batch(bf, a['lang'], a['paragraph'], a['cookies'])

    # ── URL ───────────────────────────────────────────────────────────────────
    elif target.startswith('http://') or target.startswith('https://'):
        try:
            convert_url(target, a['lang'], a['paragraph'], a['cookies'])
            ok += 1
        except Exception as e:
            log.error(f"  [FAIL] {e}")
            fail += 1

    # ── File / folder ─────────────────────────────────────────────────────────
    else:
        path = Path(target)
        if path.is_dir():
            files = list(path.glob('*.srt')) + list(path.glob('*.vtt'))
            if not files:
                log.info(f"No .srt/.vtt files found in: {path}")
                sys.exit(0)
        elif path.is_file():
            files = [path]
        else:
            log.error(f"Path not found: {target}")
            sys.exit(1)

        for f in files:
            try:
                convert_file(f, a['paragraph'])
                ok += 1
            except Exception as e:
                log.error(f"  [FAIL] {f.name}: {e}")
                fail += 1

        log.info(f"\nDone: {ok} converted, {fail} failed.")

    # ── Open output folder ────────────────────────────────────────────────────
    if a['open_output']:
        import subprocess
        subprocess.Popen(['explorer', str(OUTPUT_DIR)])


if __name__ == '__main__':
    main()