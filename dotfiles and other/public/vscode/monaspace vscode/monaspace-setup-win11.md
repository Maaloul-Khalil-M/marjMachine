# Monaspace — Full Multi-Voice Setup Guide
### Windows 11 · VS Code · JavaScript · PHP · v1.301

---

## The Full Vision

Monaspace's promise is a **typographic hierarchy for code** — not just colors, but shapes and personalities:

| Voice | Token role | Why this pairing |
|---|---|---|
| **Neon** | Variables, identifiers, body code | Clean, neutral — the silent majority of your file |
| **Argon** | Strings, template literals | Humanist, warmer — data feels different from logic |
| **Xenon** | Keywords (`const`, `function`, `class`, `return`) | Slab serif authority — structure markers stand out |
| **Radon** | Comments | Handwritten — unmistakably an aside, never mistaken for code |
| **Krypton** | Numbers, operators, punctuation, Copilot ghost text | Mechanical precision — pure data and machine logic |

Every voice shares identical glyph metrics. Mixed on the same line, indentation never breaks.

---

## What to Install

From the v1.301 release, you need:

| Zip | Install for |
|---|---|
| `monaspace-variable-v1.301.zip` | VS Code editor (all 5 voices) |
| `monaspace-nerdfonts-v1.301.zip` | Terminal icons |

**Do not install the webfont zips** (`monaspace-webfont-*`) — those are `.woff2` files for browsers only.

### Installing on Windows 11

**Variable fonts (VS Code):**
1. Extract `monaspace-variable-v1.301.zip`
2. Select all 5 `.ttf` files → right-click → **Install for all users**

**Nerd Fonts (terminal):**
1. Extract `monaspace-nerdfonts-v1.301.zip`
2. Open the `NF/` subfolder, find `MonaspaceNeonNF-Regular.otf` and `MonaspaceNeonNF-Bold.otf`
3. Right-click → **Install for all users**

> After installing, fully close and reopen VS Code. If fonts don't register, restart Windows — font caching is genuinely unreliable on Win11.

---

## settings.json

Open with `Ctrl+Shift+P` → "Open User Settings JSON":

```json
{
  "editor.fontFamily": "'Monaspace Neon Var', monospace",
  "editor.fontSize": 15,
  "editor.fontVariations": "'wght' 350",
  "editor.fontLigatures": "'calt', 'liga', 'ss01', 'ss02', 'ss03', 'ss04', 'ss07', 'cv01' 2, 'cv31' 1",
  "editor.disableMonospaceOptimizations": true,

  "editor.tokenColorCustomizations": {
    "textMateRules": [
      {
        "scope": "comment",
        "settings": { "fontStyle": "italic" }
      },
      {
        "scope": "keyword, storage.type, storage.modifier",
        "settings": { "fontStyle": "bold" }
      },
      {
        "scope": "comment.block.documentation storage, comment.block.documentation entity",
        "settings": { "fontStyle": "" }
      }
    ]
  },

  "vscode_custom_css.imports": [
    "file:///C:/Users/YOURNAME/.vscode/monaspace.css"
  ],
  "vscode_custom_css.policy": true,

  "terminal.integrated.fontFamily": "'Monaspace Neon NF'",
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.fontWeight": "500",
  "terminal.integrated.fontWeightBold": "800"
}
```

Replace `YOURNAME` with your actual Windows username.

**Why `tokenColorCustomizations` matters here:** marking keywords as `bold` and comments as `italic` via settings.json means the CSS file can catch those styles with `span[style*="font-style: italic"]` and `span[style*="font-weight: bold"]` — this is Strategy A in the CSS, and it works across all themes without needing to find MTK class numbers.

---

## The CSS File — Two Strategies Combined

Save the `monaspace.css` file (provided alongside this guide) to:

```
C:\Users\YOURNAME\.vscode\monaspace.css
```

The file uses two injection strategies:

### Strategy A — Font-style targeting (theme-agnostic)

This works with any theme, forever, no maintenance needed:

```css
/* Italic spans → Radon (comments) */
.view-line span[style*="font-style: italic"] {
  font-family: 'Monaspace Radon Var', monospace !important;
  font-size: 0.97em;
}

/* Bold spans → Xenon (keywords) */
.view-line span[style*="font-weight: bold"] {
  font-family: 'Monaspace Xenon Var', monospace !important;
  font-weight: 600;
}
```

**Trade-off:** you can only target italic and bold this way — two channels.

### Strategy B — Direct MTK class targeting (granular)

This lets you assign different voices to strings, numbers, operators, functions — any color category your theme defines. MTK classes map to theme colors, so `.mtk5` in One Dark Pro is strings (orange), but in GitHub Dark it might be keywords (red). **You must verify with DevTools.**

The CSS file includes pre-filled mappings for **One Dark Pro**, **GitHub Dark**, and **Dracula**, plus a reference block explaining what each class means in each theme.

### How to verify and fix MTK classes for your theme

1. `Help` → `Toggle Developer Tools`
2. Click the **inspector icon** (top-left of DevTools)
3. Click on a **comment** in your code → note the class on the `<span>` (e.g. `.mtk3`)
4. Click on a **string** → note its class
5. Click on a **keyword** (`const`, `function`) → note its class
6. Click on a **number** → note its class
7. Update the `STRATEGY B` section in `monaspace.css` with your class numbers

---

## Activating the CSS

1. Install **Custom CSS and JS Loader** by `be5invis` from VS Code Extensions
2. `Ctrl+Shift+P` → **Enable Custom CSS and JS**
3. Restart VS Code
4. After any future CSS edits: `Ctrl+Shift+P` → **Reload Custom CSS and JS**

> VS Code will warn about a "corrupted installation" after enabling. This is expected — click Don't Show Again.

---

## The Full Voice Map in Practice

Here's what you'll see in a JS/PHP file after setup:

```javascript
// This comment is RADON — handwritten, italic, lighter weight
// You know instantly it's an aside without reading it

const message = "Hello world";    // "Hello world" = ARGON, warmer
const count = 42;                  // 42 = KRYPTON, mechanical

function greet(name) {             // 'function' keyword = XENON, slab serif
  if (count > 0) {                 // 'if' = XENON; '>' operator = KRYPTON
    return `${message}, ${name}`   // identifier = NEON; string parts = ARGON
  }
}
```

```php
<?php // RADON comment

class UserController {            // 'class' = XENON
    private $users = [];          // '$users' = NEON; '[]' = KRYPTON

    public function getById($id) { // 'function' = XENON
        return $this->users[$id]; // '->' = KRYPTON
    }
}
```

---

## Copilot Ghost Text

The CSS targets inline suggestion spans and assigns **Krypton** to them:

```css
.ghost-text-decoration,
.suggest-preview-text,
.inline-completion-text {
  font-family: 'Monaspace Krypton Var', monospace !important;
  font-variation-settings: 'wght' 300 !important;
  opacity: 0.65;
}
```

Krypton's mechanical precision at low weight + reduced opacity = ghost text that reads as machine-generated at a glance. This is the closest VS Code currently gets to the Monaspace promo vision.

---

## Variable Weight Per Voice

Each voice gets a tuned weight in the CSS because the same `wght` value looks different across the five typefaces:

| Voice | Weight used | Reasoning |
|---|---|---|
| Neon (body code) | 350 | Slightly lighter than Regular — airy, low fatigue |
| Argon (strings) | 380 | Slightly heavier — strings should be readable but not dominant |
| Xenon (keywords) | 500 | Medium — slab serifs at 500 have authority without shouting |
| Radon (comments) | 300 | Light — handwritten + light = clearly secondary content |
| Krypton (numbers/operators) | 400 | Regular — precision and neutrality |

These are set via `font-variation-settings: 'wght' N` in the CSS, **not** via the `editor.fontVariations` setting (which only applies to the base font).

---

## Ligatures for JS + PHP

```json
"editor.fontLigatures": "'calt', 'liga', 'ss01', 'ss02', 'ss03', 'ss04', 'ss07', 'cv01' 2, 'cv31' 1"
```

| Feature | What it does | Language |
|---|---|---|
| `calt` | Texture healing | All |
| `liga` | Spacing for `///`, `\|\|`, `--` | All |
| `ss01` | `===` `!==` `=>` `??` | JavaScript |
| `ss02` | `<=` `>=` | All |
| `ss03` | `->` `~>` | PHP, Rust |
| `ss04` | `</` `/>` `<?` `?>` | PHP, HTML, JSX |
| `ss07` | `::` | PHP scope, C++ |
| `cv01 2` | Slashed zero | All |
| `cv31 1` | 6-pointed asterisk | All |

---

## Windows Terminal

Set font in Windows Terminal settings JSON (`Ctrl+,` → Open JSON file):

```json
"profiles": {
  "defaults": {
    "font": {
      "face": "Monaspace Neon NF",
      "size": 13,
      "weight": "medium"
    }
  }
}
```

**Oh My Posh** (git branch, Node/PHP version in prompt):

```powershell
# Install (PowerShell as admin)
winget install JanDeDobbeleer.OhMyPosh -s winget

# Add to $PROFILE (notepad $PROFILE)
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\jandedobbeleer.omp.json" | Invoke-Expression
```

---

## Troubleshooting

**Font falls back to Consolas**
Use the exact name `'Monaspace Neon Var'` — the `Var` suffix is how the variable font registers. Without it VS Code can't find it.

**Ligatures show as separate characters**
`fontLigatures` must be a string with feature tags in quotes: `"'calt', 'liga', 'ss01'"` — not `true`.

**CSS has no effect after editing**
Run `Ctrl+Shift+P` → **Reload Custom CSS and JS**. Reloading the window alone does nothing.

**Strategy A (italic/bold) works but Strategy B (MTK) doesn't**
Your theme's MTK class numbers are different from the defaults. Use DevTools to find yours (see the section above).

**MTK assignments broke after a VS Code update**
VS Code renumbers MTK classes occasionally. Re-inspect with DevTools and update `monaspace.css`. Takes 5 minutes.

**Radon comments look too large**
Adjust `font-size` in `.mtk3` — try `0.93em` to `0.98em`. Radon's expressive letterforms render optically larger than Neon.

**Terminal icons are squares**
You're using `Monaspace Neon Var` in the terminal instead of `Monaspace Neon NF`. They are separate font files.

---

## Honest Maintenance Notes

Strategy A (italic/bold targeting) requires zero maintenance — it survives VS Code updates.

Strategy B (MTK classes) needs re-checking after major VS Code or theme updates. This happens a few times a year and takes a few minutes each time.

The Copilot ghost text selectors (`.ghost-text-decoration`, `.suggest-preview-text`) are the most fragile — VS Code may rename these classes. If Krypton stops appearing on suggestions, inspect the ghost text element in DevTools to find the current class name and update it.
