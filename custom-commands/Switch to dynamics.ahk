#Requires AutoHotkey v2.0

SendMode("Input")  ; Режим отправки ввода
SetWorkingDir A_ScriptDir  ; Рабочая директория = папке скрипта

deviceName := "HP P27h G4"
Run('nircmd setdefaultsounddevice "' deviceName '" 1')