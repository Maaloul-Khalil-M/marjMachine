#Requires AutoHotkey v2.0
#SingleInstance Force

; ═══════════════════════════════════════════════════════════════
; ⚙️ CONFIGURATION
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