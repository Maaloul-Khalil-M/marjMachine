import ctypes
import csv
import io
import subprocess
import re
import shutil
import typer
from pathlib import Path
from typing import Optional

# ── optional QR dependency ────────────────────────────────────────────────────
try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

# Initialize Typer app
app = typer.Typer(help="Show saved Wi-Fi passwords on Windows.")

# ── helpers ───────────────────────────────────────────────────────────────────
def run_cmd(cmd: list[str]) -> str:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout

def check_admin() -> bool:
    """Use Windows API — reliable, no side effects."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def get_current_ssid() -> str | None:
    """Return the SSID of the currently connected Wi-Fi network, or None."""
    out = run_cmd(["netsh", "wlan", "show", "interfaces"])
    match = re.search(r"^\s+SSID\s*:\s*(.+)$", out, re.MULTILINE)
    return match.group(1).strip() if match else None

def get_all_profiles() -> list[str]:
    out = run_cmd(["netsh", "wlan", "show", "profiles"])
    return [p.strip() for p in re.findall(r"All User Profile\s*:\s*(.+)", out)]

def get_password(profile: str) -> str:
    out = run_cmd(["netsh", "wlan", "show", "profile", f'name="{profile}"', "key=clear"])
    match = re.search(r"Key Content\s*:\s*(.+)", out)
    return match.group(1).strip() if match else "Open / No Password"

def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Uses pyperclip if available, falls back to clip.exe."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        pass
    try:
        subprocess.run("clip", input=text, text=True, check=True)
        return True
    except Exception:
        return False

def show_qr(ssid: str, password: str) -> None:
    if not HAS_QR:
        typer.secho("  [!] Install qrcode to use --qr:  pip install qrcode[pil]", fg=typer.colors.YELLOW)
        return

    nopass = password == "Open / No Password"
    auth = "nopass" if nopass else "WPA"
    qr_data = f"WIFI:T:{auth};S:{ssid};P:{'' if nopass else password};;"

    qr = qrcode.QRCode(border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)

    typer.echo("")
    qr.print_ascii(invert=True)

def print_row(ssid: str, password: str) -> None:
    ssid_padded = f"{ssid:<35}"
    typer.echo(f"{ssid_padded} | ", nl=False)
    if password == "Open / No Password":
        typer.secho(password, fg=typer.colors.YELLOW)
    else:
        typer.secho(password, fg=typer.colors.GREEN)

def export_csv(profiles: list[str], out_path: Path) -> None:
    """Write all SSIDs and passwords to a CSV file."""
    rows = [(p, get_password(p)) for p in profiles]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["SSID", "Password"])
        writer.writerows(rows)
    typer.secho(f"  ✓ Exported {len(rows)} profiles to {out_path}", fg=typer.colors.GREEN)

# ── main ──────────────────────────────────────────────────────────────────────
@app.command()
def main(
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Filter by network name (partial match, case-insensitive)"
    ),
    qr: bool = typer.Option(
        False,
        "--qr",
        "-q",
        help="Show QR code for the matched network"
    ),
    show_all: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Show all saved networks instead of just the current one"
    ),
    copy: bool = typer.Option(
        False,
        "--copy",
        "-c",
        help="Copy the password to clipboard"
    ),
    export: Optional[Path] = typer.Option(
        None,
        "--export",
        "-e",
        help="Export all profiles to a CSV file (e.g. --export passwords.csv)"
    ),
):
    """
    Retrieves Wi-Fi profiles and plaintext passwords from Windows.

    With no arguments, shows the password for the currently connected network.
    """
    if not shutil.which("netsh"):
        typer.secho("[ERROR] netsh not found. Are you on Windows?", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    if not check_admin():
        typer.secho("[WARNING] Not running as Administrator — passwords may be hidden.\n", fg=typer.colors.YELLOW, err=True)

    profiles = get_all_profiles()
    if not profiles:
        typer.echo("No Wi-Fi profiles found.")
        raise typer.Exit()

    # ── Export mode (always uses full profile list) ───────────────────────────
    if export:
        export_csv(profiles, export)
        raise typer.Exit()

    # ── Resolve target: explicit --name > current SSID > show all ─────────────
    if not show_all:
        query_name = name or get_current_ssid()
    else:
        query_name = None

    # ── Single / filtered network ─────────────────────────────────────────────
    if query_name:
        query_lower = query_name.lower()
        matches = [p for p in profiles if query_lower in p.lower()]

        if not matches:
            typer.secho(f"[!] No profile matching '{query_name}' found.", fg=typer.colors.RED)
            typer.echo("    Available profiles:")
            for p in profiles:
                typer.echo(f"      • {p}")
            raise typer.Exit(code=1)

        for profile in matches:
            password = get_password(profile)
            print_row(profile, password)

            if copy:
                if len(matches) > 1:
                    typer.secho("  [!] --copy skipped: multiple matches found.", fg=typer.colors.YELLOW)
                elif copy_to_clipboard(password):
                    typer.secho("  ✓ Password copied to clipboard.", fg=typer.colors.GREEN)
                else:
                    typer.secho("  [!] Clipboard copy failed.", fg=typer.colors.YELLOW)

            if qr:
                show_qr(profile, password)

    # ── Show all ──────────────────────────────────────────────────────────────
    else:
        if qr:
            typer.secho("[!] --qr only works with a specific network. Showing all without QR.\n", fg=typer.colors.YELLOW)
        if copy:
            typer.secho("[!] --copy only works with a specific network. Skipping.\n", fg=typer.colors.YELLOW)

        typer.secho(f"{'Wi-Fi Network':<35} | Password", bold=True, fg=typer.colors.CYAN)
        typer.echo("-" * 60)

        for profile in profiles:
            print_row(profile, get_password(profile))

if __name__ == "__main__":
    app()