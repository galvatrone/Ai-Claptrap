#Requires AutoHotkey v2.0
SendMode("Input")
SetWorkingDir A_ScriptDir

Run("shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic")

; Ждём окно Media Player
if !WinWait("ahk_class ApplicationFrameWindow", , 10) {
    MsgBox("Media Player не открылся.")
    ExitApp
}

; Активируем
WinActivate
Sleep(2000)

; Навигация к списку
Send("^r")
;Sleep(300)
;Send("{Enter}")   ; Запускаем воспроизведение
;Sleep(300)

; Включение Shuffle
Send("^p")