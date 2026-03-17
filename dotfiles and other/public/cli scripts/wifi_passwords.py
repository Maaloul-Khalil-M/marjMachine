# wifi_passwords.py
# Usage:
#   python wifi_passwords.py                  → show all
#   python wifi_passwords.py --name "MyWiFi"  → show one
#   python wifi_passwords.py --name "MyWiFi" --qr  → show one + QR code

import subprocess
import re
import sys
import argparse
import shutil

# ── optional QR dependency ────────────────────────────────────────────────────
try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

# ── helpers ───────────────────────────────────────────────────────────────────
def run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    ).stdout

def check_admin() -> bool:
    """Heuristic: try a known admin-only netsh command and see if it errors."""
    out = run(["netsh", "wlan", "show", "profile",
               "name=__probe_admin_check__", "key=clear"])
    # If netsh says "not found" we got far enough — admin is fine
    # If it says "access is denied" we're not admin
    return "access is denied" not in out.lower()

def get_all_profiles() -> list[str]:
    out = run(["netsh", "wlan", "show", "profiles"])
    return [p.strip() for p in re.findall(r"All User Profile\s*:\s*(.+)", out)]

def get_password(profile: str) -> str:
    out = run(["netsh", "wlan", "show", "profile",
               f'name="{profile}"', "key=clear"])
    match = re.search(r"Key Content\s*:\s*(.+)", out)
    return match.group(1).strip() if match else "Open / No Password"

def show_qr(ssid: str, password: str) -> None:
    if not HAS_QR:
        print("  [!] Install qrcode to use --qr:  pip install qrcode[pil]")
        return
    # Standard Wi-Fi QR format
    nopass = password == "Open / No Password"
    auth = "nopass" if nopass else "WPA"
    qr_data = f"WIFI:T:{auth};S:{ssid};P:{'' if nopass else password};;"
    qr = qrcode.QRCode(border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr.print_ascii(invert=True)  # prints to terminal, no file needed

def print_row(ssid: str, password: str) -> None:
    print(f"{ssid:<35} | {password}")

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Show saved Wi-Fi passwords on Windows."
    )
    parser.add_argument("--name", "-n", metavar="SSID",
                        help="Filter by network name (partial match supported)")
    parser.add_argument("--qr", action="store_true",
                        help="Show QR code for the matched network")
    args = parser.parse_args()

    # Netsh must be available
    if not shutil.which("netsh"):
        print("[ERROR] netsh not found. Are you on Windows?", file=sys.stderr)
        sys.exit(1)

    # Warn if not admin (passwords will be blank otherwise)
    if not check_admin():
        print("[WARNING] Not running as Administrator — passwords may be hidden.\n",
              file=sys.stderr)

    profiles = get_all_profiles()
    if not profiles:
        print("No Wi-Fi profiles found.")
        return

    # ── filter by name ────────────────────────────────────────────────────────
    if args.name:
        query = args.name.lower()
        matches = [p for p in profiles if query in p.lower()]
        if not matches:
            print(f"[!] No profile matching '{args.name}' found.")
            print("    Available profiles:")
            for p in profiles:
                print(f"      • {p}")
            return

        for profile in matches:
            password = get_password(profile)
            print_row(profile, password)
            if args.qr:
                show_qr(profile, password)
    else:
        # ── show all ──────────────────────────────────────────────────────────
        if args.qr:
            print("[!] --qr only works with --name. Showing all without QR.\n")
        print(f"{'Wi-Fi Network':<35} | Password")
        print("-" * 60)
        for profile in profiles:
            print_row(profile, get_password(profile))

if __name__ == "__main__":
    main()