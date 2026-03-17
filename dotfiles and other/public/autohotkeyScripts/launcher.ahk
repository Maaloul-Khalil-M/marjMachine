#Requires AutoHotkey v2.0
#SingleInstance Force

; ═══════════════════════════════════════════════════════════════
; CAPSLOCK AS MODIFIER - Disable default CapsLock behavior
; ═══════════════════════════════════════════════════════════════
SetCapsLockState "AlwaysOff"

; ═══════════════════════════════════════════════════════════════
; VIM-STYLE NAVIGATION
; ═══════════════════════════════════════════════════════════════

; ───────── Navigation with Selection Support (CapsLock + IJKL)
CapsLock & i::{
    if GetKeyState("Shift", "P")
        Send "+{Up}"
    else
        Send "{Up}"
}

CapsLock & k::{
    if GetKeyState("Shift", "P")
        Send "+{Down}"
    else
        Send "{Down}"
}

CapsLock & j::{
    if GetKeyState("Shift", "P")
        Send "+{Left}"
    else
        Send "{Left}"
}

CapsLock & l::{
    if GetKeyState("Shift", "P")
        Send "+{Right}"
    else
        Send "{Right}"
}

; ───────── Word Navigation (CapsLock + H/M)
CapsLock & h::{
    if GetKeyState("Shift", "P")
        Send "^+{Left}"    ; Select word left
    else
        Send "^{Left}"     ; Jump word left
}

CapsLock & m::{
    if GetKeyState("Shift", "P")
        Send "^+{Right}"   ; Select word right
    else
        Send "^{Right}"    ; Jump word right
}

; ───────── Line Navigation (CapsLock + U/O)
CapsLock & u::{
    if GetKeyState("Shift", "P")
        Send "+{Home}"     ; Select to start
    else
        Send "{Home}"      ; Start of line
}

CapsLock & o::{
    if GetKeyState("Shift", "P")
        Send "+{End}"      ; Select to end
    else
        Send "{End}"       ; End of line
}

/*
; ───────── Page Navigation (CapsLock + Y/P)
CapsLock & y::Send "{PgUp}"
CapsLock & p::Send "{PgDn}"
*/

; ───────── Delete operations (CapsLock + D/Backspace)
CapsLock & d::Send "{Delete}"
CapsLock & Backspace::Send "^{Backspace}"

; ═══════════════════════════════════════════════════════════════
; APPLICATION LAUNCHERS - NUMPAD ONLY
; ═══════════════════════════════════════════════════════════════

; ───────── Terminals (Numpad 1-3)
CapsLock & Numpad1::Run 'wt.exe -p "PowerShell"'
CapsLock & Numpad2::Run 'wt.exe -p "git bash"'
CapsLock & Numpad3::Run 'wt.exe -p "Ubuntu"'

; ───────── Editors & Readers (Keep letter shortcuts)
CapsLock & n::Run 'C:\Program Files\Notepad++\notepad++.exe'
CapsLock & b::Run 'C:\Users\MarjPc\AppData\Local\Programs\Obsidian\Obsidian.exe'
CapsLock & r::Run 'C:\Users\MarjPc\AppData\Local\SumatraPDF\SumatraPDF.exe'

; ───────── Design & Dev
CapsLock & g::Run 'C:\Users\MarjPc\AppData\Local\Figma\app-125.11.6\Figma.exe'

; ───────── Browsers
CapsLock & f::{
    Run "firefox.exe"
    Sleep 2000
    Send "^+i"
}

CapsLock & c::{
    Run "chrome.exe"
    Sleep 2000
    Send "^+i"
}

; ═══════════════════════════════════════════════════════════════
; MUSIC MENU - CapsLock + V (VLC) using VLC from PATH
; ═══════════════════════════════════════════════════════════════

CapsLock & v::{
    MusicMenu := Menu()
    MusicMenu.Add("🎵 Lofi Music", MenuLofi)
    MusicMenu.Add("🎮 Gaming Music", MenuGaming)
    MusicMenu.Add("🎲 Random Music", MenuRandom)
    MusicMenu.Add()  ; Separator
    MusicMenu.Add("⏹ Stop VLC", MenuStopVLC)
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
; HELP MENU - CapsLock + /
; ═══════════════════════════════════════════════════════════════

CapsLock & /::{
	helpText := "
	(
	• **VIM-STYLE CAPSLOCK SHORTCUTS**

	• **BASIC NAVIGATION**
	  - CapsLock + I      → Up ↑
	  - CapsLock + K      → Down ↓
	  - CapsLock + J      → Left ←
	  - CapsLock + L      → Right →

	• **SELECTION MODE (Hold Shift)**
	  - Shift+CapsLock+I  → Select Up
	  - Shift+CapsLock+K  → Select Down
	  - Shift+CapsLock+J  → Select Left
	  - Shift+CapsLock+L  → Select Right

	• **WORD NAVIGATION**
	  - CapsLock + H      → Jump Word Left
	  - CapsLock + ;      → Jump Word Right
	  - Shift+CapsLock+H  → Select Word Left
	  - Shift+CapsLock+;  → Select Word Right

	• **LINE NAVIGATION**
	  - CapsLock + U      → Home (Start of line)
	  - CapsLock + O      → End (End of line)
	  - Shift+CapsLock+U  → Select to Start
	  - Shift+CapsLock+O  → Select to End

	• **PAGE NAVIGATION**
	  - CapsLock + Y      → Page Up
	  - CapsLock + P      → Page Down

	• **DELETE OPERATIONS**
	  - CapsLock + D      → Delete forward
	  - CapsLock + Bksp   → Delete word backward

	• **APPLICATIONS**
	  - CapsLock + Numpad1 → PowerShell 
	  - CapsLock + Numpad2 → Git Bash 
	  - CapsLock + Numpad3 → Ubuntu 
	  - CapsLock + N       → Notepad++
	  - CapsLock + B       → Obsidian (Brain)
	  - CapsLock + R       → SumatraPDF (Reader)
	  - CapsLock + G       → Figma (Graphics)
	  - CapsLock + F       → Firefox + DevTools
	  - CapsLock + C       → Chrome + DevTools

	• **SPECIAL**
	  - CapsLock + V      → Music Menu  (VLC)
	  - CapsLock + P      → PROJECT MENU
	  - CapsLock + /      → This Help Menu

	)"
	MsgBox(helpText, "VIM-Style Shortcuts", "Iconi T90")
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
    Cmd: "npm run dev" 
}
/*
; --- PROJECT 2: Laravel Backend ---
MyProjects["🐘 Laravel API"] := { 
    Path: "C:\xampp\htdocs\my-api", 
    Cmd: "php artisan serve" 
}

; --- PROJECT 3: Python Script ---
MyProjects["🐍 Data Scraper"] := { 
    Path: "C:\Scripts\scraper", 
    Cmd: "python main.py" 
}
*/
; ═══════════════════════════════════════════════════════════════
; 🧠 INTERNAL STATE (Do not edit below)
; ═══════════════════════════════════════════════════════════════
global ProjectStates := Map() ; Stores running PIDs

; ═══════════════════════════════════════════════════════════════
; ⌨️ MENU SHORTCUT - CapsLock + P
; ═══════════════════════════════════════════════════════════════
CapsLock & p::
{
    ProjectMenu := Menu()
    
    ; 1. Clean up dead PIDs
    ValidateRunningProjects()

    ; 2. Build Menu
    for name, config in MyProjects {
        ; Create a bound function passing the Name and the Config object
        handler := ToggleProject.Bind(name, config)
        
        ProjectMenu.Add(name, handler)
        
        ; Add Checkmark if running
        if ProjectStates.Has(name)
            ProjectMenu.Check(name)
    }

    ProjectMenu.Add() ; Separator
    ProjectMenu.Add("⏹ Stop All Projects", StopAllProjects)
    
    ; Disable "Stop All" if nothing is running
    if (ProjectStates.Count == 0)
        ProjectMenu.Disable("⏹ Stop All Projects")

    ProjectMenu.Show()
}

; ═══════════════════════════════════════════════════════════════
; 🚀 LOGIC FUNCTIONS
; ═══════════════════════════════════════════════════════════════

ToggleProject(name, config, *) {
    if ProjectStates.Has(name) {
        StopProject(name)
    } else {
        StartProject(name, config)
    }
}

StartProject(name, config) {
    if !DirExist(config.Path) {
        ShowTip("❌ Error: Path not found for `n" name)
        return
    }

    ; Construct the command: Change Directory -> Execute Command
    ; /k keeps the window open if it crashes immediately (for debugging), /c closes it when done.
    ; We use /c here assuming you want it backgrounded, but `cmd /c` is standard for AutoHotkey hidden runs.
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
    
    ; Force kill tree (/T) to ensure php.exe or node.exe dies, not just cmd.exe
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