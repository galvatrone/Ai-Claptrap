#Requires AutoHotkey v2.0

; Запускаем Media Player
Run("shell:AppsFolder\Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic")

; Ждём окно Media Player с классом ApplicationFrameWindow
if !WinWait("ahk_class ApplicationFrameWindow", , 10) {
    MsgBox("Media Player не открылся.")
    ExitApp
}

; Сохраняем найденное окно в переменную
playerWin := WinExist("ahk_class ApplicationFrameWindow")

; Активируем и отправляем команду
if playerWin {
    WinActivate(playerWin)
    Sleep(500)

    ; Пробуем разные сочетания клавиш
    ; Простой Right
    Send("^b")
    
    ; Или Ctrl+Right
    ; Send("^Right")
    
    ; Или Alt+Right
    ; Send("!Right")
}
