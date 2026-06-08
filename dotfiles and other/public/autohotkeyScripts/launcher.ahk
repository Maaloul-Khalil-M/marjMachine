#Requires AutoHotkey v2.0
#SingleInstance Force

; ═══════════════════════════════════════════════════════════════
; CAPSLOCK AS MODIFIER - Disable default CapsLock behavior
; ═══════════════════════════════════════════════════════════════
SetCapsLockState "AlwaysOff"

; ═══════════════════════════════════════════════════════════════
; VIM-STYLE NAVIGATION commented
; ═══════════════════════════════════════════════════════════════

; ------------------------------------------------------------
; BASIC NAVIGATION (CapsLock + IJKL)
; ------------------------------------------------------------
; CapsLock + I      → Move cursor Up
; Shift+CapsLock+I → Select Up
CapsLock & i::{
    if GetKeyState("Shift", "P")
        Send "+{Up}"
    else
        Send "{Up}"
}

; CapsLock + K      → Move cursor Down
; Shift+CapsLock+K → Select Down
CapsLock & k::{
    if GetKeyState("Shift", "P")
        Send "+{Down}"
    else
        Send "{Down}"
}

; CapsLock + J      → Move cursor Left
; Shift+CapsLock+J → Select Left
CapsLock & j::{
    if GetKeyState("Shift", "P")
        Send "+{Left}"
    else
        Send "{Left}"
}

; CapsLock + L      → Move cursor Right
; Shift+CapsLock+L → Select Right
CapsLock & l::{
    if GetKeyState("Shift", "P")
        Send "+{Right}"
    else
        Send "{Right}"
}

; ------------------------------------------------------------
; WORD NAVIGATION (CapsLock + H/M)
; ------------------------------------------------------------
; CapsLock + H      → Jump one word left
; Shift+CapsLock+H → Select one word left
CapsLock & h::{
    if GetKeyState("Shift", "P")
        Send "^+{Left}"    ; Select word left
    else
        Send "^{Left}"     ; Jump word left
}

; CapsLock + M      → Jump one word right
; Shift+CapsLock+M → Select one word right
CapsLock & m::{
    if GetKeyState("Shift", "P")
        Send "^+{Right}"   ; Select word right
    else
        Send "^{Right}"    ; Jump word right
}

; ------------------------------------------------------------
; LINE NAVIGATION (CapsLock + U/O)
; ------------------------------------------------------------
; CapsLock + U      → Move to start of line
; Shift+CapsLock+U → Select to start of line + copy to clipboard
CapsLock & u::{
    if GetKeyState("Shift", "P")
        Send "+{Home}"     ; Select to start
    else
        Send "{Home}"      ; Start of line
}

; CapsLock + O      → Move to end of line
; Shift+CapsLock+O → Select to end of line + copy to clipboard
CapsLock & o::{
    if GetKeyState("Shift", "P")
        Send "+{End}"      ; Select to end
    else
        Send "{End}"       ; End of line
}

;bruh
; copy from cursor to start of file to clipboard
^Numpad4:: {
    A_Clipboard := ""
    Send "^+{Home}^c"
    ClipWait(1)
}

; copy from cursor to end of file to clipboard
^Numpad6:: {
    A_Clipboard := ""
    Send "^+{End}^c"
    ClipWait(1)
}

; go to start of file
^Numpad7::Send "^{Home}"

; go to end of file
^Numpad9::Send "^{End}"

; ------------------------------------------------------------
; DELETE OPERATIONS (CapsLock + D/Backspace)
; ------------------------------------------------------------
; CapsLock + D      → Delete forward
CapsLock & d::Send "{Delete}"

; CapsLock + Backspace → Delete previous word
CapsLock & Backspace::Send "^{Backspace}"

; ------------------------------------------------------------
; PAGE NAVIGATION (RESERVED)
; ------------------------------------------------------------
; NOTE:
; CapsLock+P is reserved for PROJECT MENU
; Using Y and [ for page navigation instead

; CapsLock + Y      → Page Up
; CapsLock + [      → Page Down

; CapsLock & y::Send "{PgUp}"
; CapsLock & [::Send "{PgDn}"


; ═══════════════════════════════════════════════════════════════
; APPLICATION LAUNCHERS - NUMPAD ONLY
; ═══════════════════════════════════════════════════════════════

; ───────── Terminals (Numpad 1-3)
CapsLock & Numpad1::Run 'wt.exe -p "PowerShell"'
CapsLock & Numpad2::Run 'wt.exe -p "git bash"'
CapsLock & Numpad3::Run 'wt.exe -p "Ubuntu"'

; ───────── Editors & Readers
CapsLock & n::Run 'C:\Program Files\Notepad++\notepad++.exe'
CapsLock & b::Run 'C:\Users\MarjPc\AppData\Local\Programs\Obsidian\Obsidian.exe'
CapsLock & r::Run 'C:\Users\MarjPc\AppData\Local\SumatraPDF\SumatraPDF.exe'

; ───────── Design: version locked comment
;CapsLock & g::Run 'C:\Users\MarjPc\AppData\Local\Figma\app-125.11.6\Figma.exe'
; ───────── Browsers

CapsLock & f::{
    Run "firefox.exe"
    Sleep 2000
    ;Send "^+i"
}

CapsLock & c::{
    Run "chrome.exe"
    Sleep 2000
    ;Send "^+i"
}

CapsLock & Space::
{
    vscodePath := "C:\Users\" A_UserName "\AppData\Local\Programs\Microsoft VS Code\Code.exe"

    if FileExist(vscodePath)
        Run '"' vscodePath '"'
    else {
        customPath := InputBox("VS Code not found at default path.`nEnter your VS Code path manually:", "VS Code Path")
        if customPath.Result = "OK" && FileExist(customPath.Value)
            Run '"' customPath.Value '"'
        else
            MsgBox "File not found: " customPath.Value
    }
}

; ═══════════════════════════════════════════════════════════════
; MUSIC MENU - CapsLock + V (VLC)
; ═══════════════════════════════════════════════════════════════

CapsLock & v::{
    MusicMenu := Menu()
    MusicMenu.Add("🎵 Lofi Music",   MenuLofi)
    MusicMenu.Add("🎮 Gaming Music",  MenuGaming)
    MusicMenu.Add("🎲 Random Music",  MenuRandom)
    MusicMenu.Add()  ; Separator
    MusicMenu.Add("⏹ Stop VLC",      MenuStopVLC)
    MusicMenu.Show()
}

MenuLofi(*) {
    ProcessClose("vlc.exe")
    Sleep 200
    Run 'vlc "C:\music\lofi" --loop --random --qt-start-minimized --qt-system-tray --no-video'
}

MenuGaming(*) {
    ProcessClose("vlc.exe")
    Sleep 200
    Run 'vlc "C:\music\game" --loop --random --qt-start-minimized --qt-system-tray --no-video'
}

MenuRandom(*) {
    ProcessClose("vlc.exe")
    Sleep 200
    Run 'vlc "C:\music\random" --loop --random --qt-start-minimized --qt-system-tray --no-video'
}

MenuStopVLC(*) {
    ProcessClose("vlc.exe")
}

; ═══════════════════════════════════════════════════════════════
; GAME MENU - CapsLock + X
; FIX: was defined as a Map but never wired to a hotkey or menu.
; Wired it up here to match the VLC/Project menu pattern.
; ═══════════════════════════════════════════════════════════════

global GamesList := [
    ["Pinball",            "C:\Users\MarjPc\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Games\Pinball.lnk"],
    ["Chess",              "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Chess.lnk"],
    ["Hearts",             "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Hearts.lnk"],
    ["Minesweeper",        "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Minesweeper.lnk"],
    ["Solitaire",          "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Solitaire.lnk"],
    ["FreeCell",           "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\FreeCell.lnk"],
    ["Mahjong",            "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Mahjong.lnk"],
    ["Purble Place",       "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Purble Place.lnk"],
    ["Spider Solitaire",   "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Games\Spider Solitaire.lnk"]
]

CapsLock & x::{
    GameMenu := Menu()

    for game in GamesList {
        label := game[1]
        path  := game[2]

        handler := LaunchGame.Bind(path)
        GameMenu.Add(label, handler)

        if !FileExist(path)
            GameMenu.Disable(label)
    }

    GameMenu.Show()
}

LaunchGame(path, *) {
    if FileExist(path)
        Run path
    else
        MsgBox "Game not found at:`n" path, "Game Launcher", "Iconx"
}
; ═══════════════════════════════════════════════════════════════
; HELP MENU - CapsLock + /
; ═══════════════════════════════════════════════════════════════

CapsLock & /::{
    helpText := "
    (
• APPLICATIONS
  - CapsLock + Numpad1 → PowerShell
  - CapsLock + Numpad2 → Git Bash
  - CapsLock + Numpad3 → Ubuntu
  - CapsLock + N       → Notepad++
  - CapsLock + B       → Obsidian (Brain)
  - CapsLock + R       → SumatraPDF (Reader)
  - CapsLock + G       → Figma (auto-detects version)
  - CapsLock + F       → Firefox + DevTools
  - CapsLock + C       → Chrome + DevTools
  - CapsLock + Space   → VS Code

• MENUS
  - CapsLock + V       → Music Menu (VLC)
  - CapsLock + P       → Project Menu
  - CapsLock + X       → Game Menu
  - CapsLock + /       → This Help Menu

• VIM NAVIGATION  (uncomment block to enable)
  - CapsLock + I/K/J/L → ↑ ↓ ← →
  - CapsLock + H/M     → Word ← / →
  - CapsLock + U/O     → Home / End
  - Hold Shift + above → Selection mode
  - CapsLock + D       → Delete forward
  - CapsLock + Bksp    → Delete word backward
    )"
    MsgBox(helpText, "CapsLock Shortcuts", "Iconi T90")
}

; ═══════════════════════════════════════════════════════════════
; CONFIGURATION
; Define your projects here.
; format: "UniqueName", { Path: "...", Cmd: "..." }
; ═══════════════════════════════════════════════════════════════
MyProjects := Map()

; --- PROJECT 1: React Frontend ---
MyProjects["🌐 TutorielHell"] := {
    Path: "E:\post annee blanche\tutorielHell",
    Cmd:  "npm run dev"
}
/*
; --- PROJECT 2: Laravel Backend ---
MyProjects["🐘 Laravel API"] := {
    Path: "C:\xampp\htdocs\my-api",
    Cmd:  "php artisan serve"
}

; --- PROJECT 3: Python Script ---
MyProjects["🐍 Data Scraper"] := {
    Path: "C:\Scripts\scraper",
    Cmd:  "python main.py"
}
*/

; ═══════════════════════════════════════════════════════════════
; INTERNAL STATE (Do not edit below)
; ═══════════════════════════════════════════════════════════════
global ProjectStates := Map()

; ═══════════════════════════════════════════════════════════════
; PROJECT MENU - CapsLock + P
; ═══════════════════════════════════════════════════════════════
CapsLock & p::
{
    ProjectMenu := Menu()

    ValidateRunningProjects()

    for name, config in MyProjects {
        handler := ToggleProject.Bind(name, config)
        ProjectMenu.Add(name, handler)
        if ProjectStates.Has(name)
            ProjectMenu.Check(name)
    }

    ProjectMenu.Add()
    ProjectMenu.Add("⏹ Stop All Projects", StopAllProjects)

    if (ProjectStates.Count == 0)
        ProjectMenu.Disable("⏹ Stop All Projects")

    ProjectMenu.Show()
}

; ═══════════════════════════════════════════════════════════════
; PROJECT LOGIC FUNCTIONS
; ═══════════════════════════════════════════════════════════════

ToggleProject(name, config, *) {
    if ProjectStates.Has(name)
        StopProject(name)
    else
        StartProject(name, config)
}

StartProject(name, config) {
    if !DirExist(config.Path) {
        ShowTip("❌ Error: Path not found for `n" name)
        return
    }

    fullCmd := 'cmd.exe /c cd /d "' config.Path '" && ' config.Cmd

    try {
        Run fullCmd, config.Path, "Hide", &pid
        ProjectStates[name] := pid
        ShowTip("🚀 " name " Started `nPID: " pid)
    } catch as e {
        ShowTip("❌ Failed to start " name)
    }
}

StopProject(name) {
    if !ProjectStates.Has(name)
        return

    pid := ProjectStates[name]
    RunWait 'taskkill /PID ' pid ' /T /F',, "Hide"
    ProjectStates.Delete(name)
    ShowTip("🛑 " name " Stopped")
}

StopAllProjects(*) {
    count := ProjectStates.Count
    if (count == 0) {
        ShowTip("Nothing to stop.")
        return
    }

    names := []
    for name, pid in ProjectStates
        names.Push(name)

    for name in names
        StopProject(name)

    ShowTip("🛑 All " count " projects stopped.")
}

ValidateRunningProjects() {
    CleanList := []
    for name, pid in ProjectStates {
        if !ProcessExist(pid)
            CleanList.Push(name)
    }
    for name in CleanList
        ProjectStates.Delete(name)
}

ShowTip(text) {
    ToolTip text
    SetTimer () => ToolTip(), -2000
}

; ═══════════════════════════════════════════════════════════════
; TUTOR MODE PROMPT - Ctrl+Alt+A
; ═══════════════════════════════════════════════════════════════

^!a::
{
    tutorPrompt := "
    (
[TUTOR MODE - READ BEFORE ANSWERING]

You are a Socratic CS mentor. Your ONLY job is to help me think, NOT to solve this for me.

RULES (non-negotiable):
- DO NOT give me the solution or fixed code directly.
- DO NOT write corrected code even if I beg. Say ""I won't do that yet.""
- Start by asking: ""What's your current understanding of what's going wrong?""
- Guide me through these stages IN ORDER:
  1. Diagnose: What does the error say? What line? What type?
  2. Hypothesize: What are 2-3 possible causes?
  3. Isolate: What's the smallest test to confirm the cause?
  4. Research: What docs, search, or print statement would help?
  5. Attempt: Only after I've tried, give a hint (pseudocode only, not code).
- If I say ""just tell me"" or ""I give up"": ""You're closer than you think. What did step [X] reveal?""
- Only reveal the solution after I've made a real attempt and explained my reasoning.

Negative constraints:
- No ""here's the fixed version:""
- No full code blocks as first response
- No skipping stages because ""it's a small bug""

My problem:
    )"
    A_Clipboard := tutorPrompt
    Send "^v"
}

; ═══════════════════════════════════════════════════════════════════
; komorebi.ahk — AZERTY French layout
; Start with: komorebic start --ahk
; ═══════════════════════════════════════════════════════════════════
#Requires AutoHotkey v2.0.2
#SingleInstance Force

Komorebic(cmd) {
    RunWait(format("komorebic.exe {}", cmd), , "Hide")
}

; ═══════════════════════════════════════════════════════════════════
; WINDOW ACTIONS
;   Alt+Q       → close focused window
;   Alt+M       → toggle minimize: minimizes if visible, restores if minimized
; ═══════════════════════════════════════════════════════════════════
!q::Komorebic("close")

; ──minimize 

!m::Komorebic("minimize")

; ═══════════════════════════════════════════════════════════════════
; FOCUS WINDOWS
;   Alt+H/J/K/L     → focus left / down / up / right
;   Alt+ù           → cycle focus to previous window
;   Alt+Shift+ù     → cycle focus to next window
; ═══════════════════════════════════════════════════════════════════
!h::Komorebic("focus left")
!j::Komorebic("focus down")
!k::Komorebic("focus up")
!l::Komorebic("focus right")
!ù::Komorebic("cycle-focus previous")
!+ù::Komorebic("cycle-focus next")

; ═══════════════════════════════════════════════════════════════════
; MOVE WINDOWS
;   Alt+Shift+H/J/K/L   → move window left / down / up / right
;   Alt+Shift+Enter     → promote to master (BSP only)
;   Alt+Ctrl+,          → cycle-move window backward in layout order
;   Alt+Ctrl+.          → cycle-move window forward in layout order
; ═══════════════════════════════════════════════════════════════════
!+h::Komorebic("move left")
!+j::Komorebic("move down")
!+k::Komorebic("move up")
!+l::Komorebic("move right")
!+Enter::Komorebic("promote")

; AZERTY: Ctrl+Alt+, and Ctrl+Alt+; (avoiding Shift+, = < which conflicts)
!^,::Komorebic("cycle-move previous")
!^;::Komorebic("cycle-move next")

; ═══════════════════════════════════════════════════════════════════
; STACK WINDOWS
;   Alt+Arrows      → stack window in that direction
;   Alt+Escape      → unstack focused window
;   Alt+[           → cycle stack focus to previous  (use ^ for AZERTY if needed)
;   Alt+]           → cycle stack focus to next
;   Alt+Shift+A     → stack ALL windows on workspace
;   Alt+Shift+Z     → unstack ALL windows
; ═══════════════════════════════════════════════════════════════════
!Left::Komorebic("stack left")
!Down::Komorebic("stack down")
!Up::Komorebic("stack up")
!Right::Komorebic("stack right")
!Escape::Komorebic("unstack")
!+Left::Komorebic("cycle-stack previous")   ; fixed: was backwards
!+Right::Komorebic("cycle-stack next")      ; fixed: was backwards
!+a::Komorebic("stack-all")
!+z::Komorebic("unstack-all")

; ═══════════════════════════════════════════════════════════════════
; RESIZE
;   Alt+=           → widen container (horizontal increase)
;   Alt+-           → narrow container (horizontal decrease)
;   Alt+Shift+=     → grow container taller (vertical increase)
;   Alt+Shift+-     → shrink container (vertical decrease)
; ═══════════════════════════════════════════════════════════════════
!=::Komorebic("resize-axis horizontal increase")
!-::Komorebic("resize-axis horizontal decrease")
!+=::Komorebic("resize-axis vertical increase")
!+_::Komorebic("resize-axis vertical decrease")

; ═══════════════════════════════════════════════════════════════════
; WINDOW STATE TOGGLES
;   Alt+T           → toggle-float
;   Alt+Shift+F     → toggle-monocle
;   Alt+Shift+X     → toggle-maximize (Win32 native)
;   Alt+Shift+W     → toggle-tiling on/off for workspace
; ═══════════════════════════════════════════════════════════════════
!t::Komorebic("toggle-float")
!+f::Komorebic("toggle-monocle")
!+x::Komorebic("toggle-maximize")
!+w::Komorebic("toggle-tiling")

; ═══════════════════════════════════════════════════════════════════
; RESCUE / FIX
;   Alt+R           → retile (redraw all windows)
;   Alt+Shift+R     → full nuke: retile + restore-windows + reload-config
;   Alt+Ctrl+S      → quick-save-resize (snapshot ratios)
;   Alt+Ctrl+R      → quick-load-resize (restore ratios)
; ═══════════════════════════════════════════════════════════════════
!r::Komorebic("retile")
!+r::{
    Komorebic("retile")
    Sleep(150)
    Komorebic("restore-windows")
    Sleep(150)
    Komorebic("reload-configuration")
}
!^s::Komorebic("quick-save-resize")
!^r::Komorebic("quick-load-resize")

; ═══════════════════════════════════════════════════════════════════
; FOCUS WORKSPACES  (AZERTY number row)
;   Alt+&/é/"/'/( → focus workspace 0–4
;   Alt+<          → cycle to previous workspace
;   Alt+²          → cycle to next workspace
; ═══════════════════════════════════════════════════════════════════
!&::Komorebic("focus-workspace 0")
!é::Komorebic("focus-workspace 1")
!"::Komorebic("focus-workspace 2")
!'::Komorebic("focus-workspace 3")
!(::Komorebic("focus-workspace 4")
!<::Komorebic("cycle-workspace previous")
!²::Komorebic("cycle-workspace next")

; ═══════════════════════════════════════════════════════════════════
; MOVE WINDOWS TO WORKSPACES
;   Alt+Shift+&/é/"/'/( → send window to workspace 0–4
;   Alt+Shift+<          → cycle-send to previous workspace
;   Alt+Shift+²          → cycle-send to next workspace
; ═══════════════════════════════════════════════════════════════════
!+&::Komorebic("move-to-workspace 0")
!+é::Komorebic("move-to-workspace 1")
!+"::Komorebic("move-to-workspace 2")
!+'::Komorebic("move-to-workspace 3")
!+(::Komorebic("move-to-workspace 4")
!+<::Komorebic("cycle-move-to-workspace previous")
!+²::Komorebic("cycle-move-to-workspace next")

; ═══════════════════════════════════════════════════════════════════
; HELP  —  CapsLock+LAlt
; ═══════════════════════════════════════════════════════════════════
CapsLock & LAlt::
{
    helpText := "
(
WINDOW ACTIONS                  FOCUS
Alt+Q        Close window        Alt+H/J/K/L  Focus direction
Alt+M        Toggle minimize     Alt+ù        Cycle focus prev
                                 Alt+Shift+ù  Cycle focus next

MOVE                            STACK
Alt+Shift+H/J/K/L  Move dir     Alt+Arrows   Stack direction
Alt+Shift+Enter    Promote       Alt+Escape   Unstack window
Alt+Ctrl+,         Cycle prev    Alt+Shift+←  Cycle stack prev
Alt+Ctrl+;         Cycle next    Alt+Shift+→  Cycle stack next
                                 Alt+Shift+A  Stack ALL
                                 Alt+Shift+Z  Unstack ALL

RESIZE                          WINDOW STATE
Alt+=        Widen               Alt+T        Float toggle
Alt+-        Narrow              Alt+Shift+F  Monocle
Alt+Shift+=  Taller              Alt+Shift+X  Maximize
Alt+Shift+-  Shorter             Alt+Shift+W  Toggle tiling

WORKSPACES                      RESCUE / FIX
Alt+&/é/"/'/( Focus WS 0–4      Alt+R        Retile
Alt+<         Prev workspace     Alt+Shift+R  Full nuke
Alt+²         Next workspace     Alt+Ctrl+S   Save snapshot
Alt+Shift+num Move to WS         Alt+Ctrl+R   Load snapshot
Alt+Shift+<   Cycle send prev
Alt+Shift+²   Cycle send next
)"
    MsgBox(helpText, "komorebi keybinds", "OK")
}
