#Requires AutoHotkey v2.0

SendMode("Input")  ; Режим отправки ввода
SetWorkingDir A_ScriptDir  ; Рабочая директория = папке скрипта

deviceName := "HeadPhones"
Run('nircmd setdefaultsounddevice "' deviceName '" 1')
