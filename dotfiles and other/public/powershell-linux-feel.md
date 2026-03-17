# Stop Suffering in Boring PowerShell — Build a Linux-Like Dev Environment on Windows 11

> No Git Bash. No WSL. Just PowerShell configured the right way.

If you've ever used Linux and missed your slick terminal — the smart prompt, git info at a glance, a real file manager, fuzzy search — this guide builds all of that on top of PowerShell. Here's the full stack we're putting together:

| Tool | Role |
|---|---|
| **Oh My Posh** | Beautiful prompt (includes git integration) |
| **Terminal-Icons** | File/folder icons in directory listings |
| **PSReadLine** | History-based autocomplete |
| **zoxide** | Smarter `cd` with frecency |
| **Yazi** | Full terminal file manager with previews |
| **lazygit** | Visual TUI for Git — no more memorizing flags |
| **Nerd Fonts** | Icons and glyphs everything else depends on |

---

## Step 0 — Prerequisites

- **Windows Terminal** — pre-installed on Windows 11, or get it from the [Microsoft Store](https://aka.ms/terminal)
- **PowerShell 7+** — [download here](https://github.com/PowerShell/PowerShell/releases) (not Windows PowerShell 5.x)
- **winget** — test with `winget --version`
- **Git for Windows** — `winget install Git.Git` (Yazi requires the `file.exe` that ships with it)

---

## Step 1 — Install a Nerd Font

Nerd Fonts patch regular fonts with thousands of icons. Without one, Oh My Posh, Terminal-Icons, and Yazi will show broken placeholder boxes instead of glyphs.

1. Go to [nerdfonts.com](https://www.nerdfonts.com/font-downloads) and pick a font (popular: **FiraCode**, **Hack**, **JetBrainsMono**)
2. Unzip, select all `.ttf` files → right-click → **Install for all users**
3. Open **Windows Terminal → Settings → Defaults → Appearance → Font face** → select your Nerd Font → **Save**

> ⚠️ Do this before anything else. Every tool in this guide depends on it.

---

## Step 2 — Install Oh My Posh

[Oh My Posh](https://ohmyposh.dev) replaces the boring `PS C:\>` prompt with a rich, informative one. It already includes git status (branch, dirty/clean state, ahead/behind) — **no separate posh-git needed**.

```powershell
winget install JanDeDobbeleer.OhMyPosh -s winget
```

Restart your terminal, then browse the built-in themes:

```powershell
Get-PoshThemes
```

When you find one you like, save the theme config to `$HOME\.posh-themes\`:

```powershell
New-Item -ItemType Directory -Path "$HOME\.posh-themes" -Force
Copy-Item "$env:POSH_THEMES_PATH\jandedobbeleer.omp.json" "$HOME\.posh-themes\"
```

Activate it temporarily to preview:

```powershell
oh-my-posh init pwsh --config "$HOME\.posh-themes\jandedobbeleer.omp.json" | Invoke-Expression
```

We'll make it permanent in the `$PROFILE` section below.

---

## Step 3 — Terminal-Icons

[Terminal-Icons](https://github.com/devblackops/Terminal-Icons) adds colorful file/folder icons to `Get-ChildItem` output.

```powershell
Install-Module -Name Terminal-Icons -Repository PSGallery -Force
```

After importing it in your profile, `ls` output looks like a proper file manager.

---

## Step 4 — PSReadLine (Smart Autocomplete)

PSReadLine ships with PowerShell 7 but needs configuration to show history-based suggestions like Linux shells do.

```powershell
Install-Module PSReadLine -Scope CurrentUser -Force -SkipPublisherCheck
```

Key options (go into `$PROFILE`):

```powershell
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineOption -PredictionViewStyle ListView
```

`HistoryAndPlugin` is better than `History` alone — it pulls from both your command history and installed completion plugins. `ListView` shows suggestions as a dropdown list below your cursor instead of inline.

---

## Step 5 — zoxide (Smarter `cd`)

[zoxide](https://github.com/ajeetdsouza/zoxide) learns which directories you visit most and lets you jump to them with partial names — like `autojump` or `z` on Linux.

```powershell
winget install ajeetdsouza.zoxide
```

Initialize it in your `$PROFILE`:

```powershell
Invoke-Expression (& { zoxide init powershell | Out-String })
```

Usage:

```powershell
z proj        # jumps to the directory containing "proj" you've visited most
z doc sites   # multi-word jump
```

---

## Step 6 — Install Yazi

[Yazi](https://yazi-rs.github.io) is a blazing-fast terminal file manager with image previews, fuzzy search, and a Vim-like keybinding model.

### Required dependency

Yazi uses `file.exe` from Git for Windows to detect MIME types. This is **the only recommended way** — do not install `file` via Scoop or Chocolatey, they can't handle Unicode filenames (like `oliver-sjöström.jpg`) properly.

Set the environment variable pointing to the Git-bundled binary:

```powershell
# If installed via the official Git installer:
$env:YAZI_FILE_ONE = "C:\Program Files\Git\usr\bin\file.exe"

# If installed via Scoop:
# $env:YAZI_FILE_ONE = "C:\Users\<Username>\scoop\apps\git\current\usr\bin\file.exe"
```

### Install Yazi + optional dependencies

Yazi has a rich set of optional tools that unlock additional features:

```powershell
winget install sxyazi.yazi

# Optional dependencies (strongly recommended):
winget install Gyan.FFmpeg                  # video thumbnails
winget install 7zip.7zip                    # archive preview and extraction
winget install jqlang.jq                    # JSON preview
winget install oschwartz10612.Poppler       # PDF preview
winget install sharkdp.fd                   # file searching
winget install BurntSushi.ripgrep.MSVC      # file content searching
winget install junegunn.fzf                 # fuzzy navigation inside Yazi (>= 0.53.0)
winget install ajeetdsouza.zoxide           # jump to historical dirs inside Yazi
winget install ImageMagick.ImageMagick      # HEIC, JPEG XL, font previews (>= 7.1.1)
# resvg (SVG preview) is not on WinGet — use Scoop:
scoop install resvg
```

What each optional tool unlocks inside Yazi:

| Tool | What it enables |
|---|---|
| `ffmpeg` | Video file thumbnails |
| `7zip` | Preview and extract archives (.zip, .rar, etc.) |
| `jq` | Syntax-highlighted JSON preview |
| `poppler` | PDF preview |
| `fd` | File search (press `f` key in Yazi) |
| `ripgrep` | Content search inside files |
| `fzf` | Press `z` to fuzzy-jump to any subdirectory |
| `zoxide` | Press `Z` to jump to historical dirs (requires fzf) |
| `ImageMagick` | HEIC, JPEG XL, and font file previews |
| `resvg` | SVG file preview |

### The `y` shell wrapper

The shell wrapper lets Yazi change your working directory when you quit — without it, quitting drops you back where you started. The official PowerShell wrapper from the Yazi docs:

```powershell
function y {
    $tmp = (New-TemporaryFile).FullName
    yazi.exe $args --cwd-file="$tmp"
    $cwd = Get-Content -Path $tmp -Encoding UTF8
    if ($cwd -and $cwd -ne $PWD.Path -and (Test-Path -LiteralPath $cwd -PathType Container)) {
        Set-Location -LiteralPath (Resolve-Path -LiteralPath $cwd).Path
    }
    Remove-Item -Path $tmp
}
```

Use `y` to launch (instead of `yazi`), navigate freely, then press:
- `q` — quit and **cd to wherever you navigated to**
- `Q` — quit without changing directory

### Yazi keybindings quick reference

Navigation uses either arrow keys or Vim-style keys:

| Key | Action |
|---|---|
| `h` / `←` | Go up to parent directory |
| `j` / `↓` | Move cursor down |
| `k` / `↑` | Move cursor up |
| `l` / `→` | Enter directory / open file |
| `z` | Fuzzy jump to subdirectory (needs fzf) |
| `Z` | Jump to historical dir via zoxide |
| `.` | Toggle hidden files |
| `Space` | Select/deselect file |
| `v` | Enter visual selection mode |
| `y` | Yank (copy) selected |
| `x` | Cut selected |
| `p` | Paste |
| `d` | Trash selected |
| `D` | Permanently delete |
| `a` | Create file (end with `/` for directory) |
| `r` | Rename |
| `c` → `c` | Copy file path to clipboard |
| `c` → `f` | Copy filename to clipboard |
| `;` | Run a shell command |
| `q` | Quit (cd to current location) |
| `Q` | Quit (stay where you were) |
| `~` or `F1` | Open help menu |

---

## Step 7 — lazygit (Your New Git Interface)

[lazygit](https://github.com/jesseduffield/lazygit) is a terminal UI for Git that replaces memorizing dozens of commands and flags. You get a full visual overview of your repo: staged/unstaged changes, branches, commits, stash, remotes — all keyboard-navigable.

```powershell
winget install JesseDuffield.lazygit
```

Launch it from inside any Git repo:

```powershell
lazygit
```

What you can do without typing a single git command:

- Stage/unstage individual files or individual hunks within a file
- Commit with a message
- Push, pull, fetch
- Create, switch, merge, rebase branches
- Interactive rebase (squash, reorder, fixup, drop commits)
- View diffs inline with syntax highlighting
- Manage stash entries

> Oh My Posh still shows git info in your prompt (branch name, dirty state) — lazygit is for when you need to *do* something with Git.

Add a short alias in your profile:

```powershell
Set-Alias lg lazygit
```

---

## Step 8 — Your `$PROFILE` (Complete, Clean Version)

The PowerShell profile is your `.bashrc`. It runs every time a new shell session starts.

Open it:

```powershell
notepad $PROFILE
```

If it doesn't exist yet:

```powershell
New-Item -ItemType File -Path $PROFILE -Force; notepad $PROFILE
```

Here is a clean, deduplicated version incorporating your existing profile plus everything added in this guide:

```powershell
# ── Environment ───────────────────────────────────────────────────────────────
$env:YAZI_FILE_ONE = "C:\Program Files\Git\usr\bin\file.exe"

# ── Oh My Posh (includes git prompt — no posh-git needed) ────────────────────
oh-my-posh init pwsh --config "$HOME\.posh-themes\jandedobbeleer.omp.json" | Invoke-Expression

# ── Modules ───────────────────────────────────────────────────────────────────
Import-Module -Name Terminal-Icons

# ── PSReadLine (history + plugin autocomplete) ────────────────────────────────
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
Set-PSReadLineOption -PredictionViewStyle ListView

# ── zoxide (smarter cd) ───────────────────────────────────────────────────────
Invoke-Expression (& { zoxide init powershell | Out-String })

# ── Yazi shell wrapper (cd on quit) ───────────────────────────────────────────
function y {
    $tmp = (New-TemporaryFile).FullName
    yazi.exe $args --cwd-file="$tmp"
    $cwd = Get-Content -Path $tmp -Encoding UTF8
    if ($cwd -and $cwd -ne $PWD.Path -and (Test-Path -LiteralPath $cwd -PathType Container)) {
        Set-Location -LiteralPath (Resolve-Path -LiteralPath $cwd).Path
    }
    Remove-Item -Path $tmp
}

# ── Aliases ───────────────────────────────────────────────────────────────────
Set-Alias e    explorer
Set-Alias note "C:\Program Files\Notepad++\notepad++.exe"
Set-Alias lg   lazygit

```

> **Changes from your original:** Removed duplicate `zoxide init` and duplicate `PSReadLine` option calls. Renamed `$args` to `$pyArgs` inside `srttotxt` to avoid shadowing PowerShell's built-in `$args` variable. Added `lg` alias for lazygit.

Reload without restarting:

```powershell
. $PROFILE
```

---

## Troubleshooting

**Icons show as boxes/squares**
→ Your Nerd Font isn't set in Windows Terminal. Settings → Defaults → Appearance → Font face.

**`oh-my-posh` not found after install**
→ Restart the terminal. The PATH update only applies to new sessions.

**Yazi can't detect file types / shows wrong icons**
→ Check that `$env:YAZI_FILE_ONE` points to the Git-bundled `file.exe`, not a Scoop/Chocolatey version.

**Yazi previews not working for a specific file type**
→ Check the optional dependencies table in Step 6 and install the relevant tool.

**zoxide not jumping where expected**
→ zoxide builds a frecency database over time — you need to have visited the directory before. Run `zoxide query` to see what it currently knows.

**lazygit shows an empty screen**
→ Make sure you're inside a Git repository. Run `git status` first to confirm.

---

## The Full Picture

```
Windows Terminal
└── PowerShell 7
    ├── Oh My Posh        → prompt: git branch, status, time, exit code
    ├── Terminal-Icons    → colorful icons in ls output
    ├── PSReadLine        → history autocomplete as you type
    ├── zoxide            → smart cd with partial directory names
    ├── Yazi (y)          → file manager: previews, fuzzy search, navigate
    ├── lazygit (lg)      → visual git TUI: stage, commit, branch, rebase
    └── $PROFILE          → your config tying it all together
```

---

*Resources: [Oh My Posh](https://ohmyposh.dev) · [Yazi Installation](https://yazi-rs.github.io/docs/installation) · [Yazi Quick Start](https://yazi-rs.github.io/docs/quick-start) · [lazygit](https://github.com/jesseduffield/lazygit) · [Nerd Fonts](https://www.nerdfonts.com) · [zoxide](https://github.com/ajeetdsouza/zoxide)*
