# myScripts in C:\Scripts

A collection of personal CLI tools for productivity, media management, and system utilities.

---

## Table of Contents

- [getpl](#getpl) — Generate M3U8 playlists from folders
- [lenvid](#lenvid) — Calculate total video duration
- [srttotxt](#srttotxt) — Convert subtitles to plain text
- [wifipass](#wifipass) — Retrieve Wi-Fi passwords
- [study](#study) — Track study sessions and streaks

---

## getpl

Generates a single M3U8 playlist from a root folder and its 1st-level subdirectories.

```
getpl [OPTIONS] [PATH]
```

| Argument / Option | Short | Description |
|---|---|---|
| `path` | | Target root folder (default: `.`) |
| `--title` | `-t` | Custom title for the playlist file |
| `--sort` | `-s` | Force alphabetical sorting of video files |

**Examples:**

```bash
# Generate playlist from current directory
getpl

# Generate playlist from a specific course folder with a custom title
getpl "C:\Courses\Python101" -t "Python 101"

# Generate playlist with alphabetically sorted videos
getpl "C:\Courses\Python101" -s
```

---

## lenvid

Scans a directory recursively and outputs the total duration of all `.mp4` files.

```
lenvid [OPTIONS] [PATH]
```

| Argument | Description |
|---|---|
| `path` | Target directory to scan (default: `.`) |

**Examples:**

```bash
# Scan current directory
lenvid

# Scan a specific folder
lenvid "C:\Courses\Python101"
```

---

## srttotxt

Converts `.srt` / `.vtt` subtitle files or YouTube URLs to clean `.txt` files.

```
srttotxt [OPTIONS] TARGET
```

| Argument / Option | Short | Description |
|---|---|---|
| `target` | | URL, local `.srt`/`.vtt` file, folder, or batch `.txt` file *(required)* |
| `--lang` | | Language code for yt-dlp subtitles (default: `en`) |
| `--paragraph` | | Format output as a single paragraph |
| `--cookies` | | Use Chrome browser cookies for YouTube |
| `--open` | | Open output folder when done |
| `--batch` | | Treat target as a batch `.txt` file of URLs |

**Examples:**

```bash
# Convert a local .srt file
srttotxt subtitles.srt

# Download and convert subtitles from a YouTube URL
srttotxt https://youtube.com/watch?v=xxxxx

# Download Arabic subtitles from YouTube
srttotxt https://youtube.com/watch?v=xxxxx --lang ar

# Process a batch of YouTube URLs from a .txt file
srttotxt urls.txt --batch

# Output as a single paragraph and open the result folder
srttotxt subtitles.srt --paragraph --open
```

---

## wifipass

Retrieves Wi-Fi profiles and plaintext passwords from Windows. With no arguments, shows the password for the currently connected network.

```
wifipass [OPTIONS]
```

| Option | Short | Description |
|---|---|---|
| `--name` | `-n` | Filter by network name (partial match, case-insensitive) |
| `--qr` | `-q` | Show QR code for the matched network |
| `--all` | `-a` | Show all saved networks |
| `--copy` | `-c` | Copy the password to clipboard |
| `--export` | `-e` | Export all profiles to a CSV file |

**Examples:**

```bash
# Show password for currently connected network
wifipass

# Look up a specific network by name
wifipass -n "HomeNetwork"

# Show QR code for a network
wifipass -n "HomeNetwork" -q

# Copy current network's password to clipboard
wifipass -c

# Show all saved networks
wifipass -a

# Export all profiles to CSV
wifipass --export passwords.csv
```

---

## study

A session tracker for monitoring study time, streaks, and progress toward daily goals.

```
study <command> [options]
```

| Command | Description |
|---|---|
| `study start [topic]` | Start a study session |
| `study stop` | Stop and save the current session |
| `study status` | Show current session and today's progress |
| `study review [days]` | Show history for the last N days (default: 7) |
| `study streak` | Show current and longest study streak |
| `study topics` | Show time spent per topic |
| `study goal [minutes]` | Set or check your daily goal (default: 60 min) |
| `study history [limit]` | Show the last N individual sessions (default: 10) |
| `study reset` | ⚠️ Clear all session data (cannot be undone) |

**Examples:**

```bash
# Start a session on a specific topic
study start "Linear Algebra"

# Check current session and today's total
study status

# Stop and save the session
study stop

# Review the last 14 days
study review 14

# Set a daily goal of 90 minutes
study goal 90

# View time breakdown by topic
study topics

# Check your streak
study streak
```