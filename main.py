from stt.recognize import  recognize_continuous , recognize_wake_up

import random
import tts


import queue
import re
import time
from time import sleep as pause
import os

import yaml
from fuzzywuzzy import fuzz
import torch
import subprocess

import simpleaudio as sa

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

 
 # в будущем можно будет сделать несколько потоков для распознавания речи и обработки команд 
 # чем больше потоков тем больше нагрузка на процессор и память
 # больше пользователей говорят одновремено то больше потоков распознавания разношо голоса 

print("Загрузка TTS модели...")
model = torch.hub.load('snakers4/silero-models', 'silero_tts', language='ru')
 # или 'cuda', если есть GPU
print("Модель загружена и готова к работе.")

CDIR = os.path.dirname(os.path.abspath(__file__))  # Получаем текущую директорию

VA_CMD_LIST = yaml.safe_load(
    open(os.path.join(CDIR, 'commands.yaml'), 'rt', encoding='utf8'),
)



def play(phrase, wait_done=True):
    global recorder
    filename = f"{CDIR}\\sound\\"

    if phrase == "greet":
        filename += f"greet{random.choice([1, 2, 3])}.wav"
    elif phrase == "ok":
        filename += f"ok{random.choice([1, 2, 3])}.wav"
    elif phrase == "not_found":
        filename += "not_found.wav"
    elif phrase == "thanks":
        filename += "thanks.wav"
    elif phrase == "run":
        filename += "run.wav"
    elif phrase == "stupid":
        filename += "stupid.wav"
    elif phrase == "ready":
        filename += "ready.wav"
    elif phrase == "off":
        filename += "off.wav"

    if wait_done:
        recorder.stop()

    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()

    if wait_done:
        play_obj.wait_done()
        recorder.start()

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc




def execute_cmd(cmd: str, voice: str):
    if cmd == 'open_browser':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Run browser.exe'])
        play("test")

    elif cmd == 'open_youtube':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Run youtube.exe'])
        play("test")

    elif cmd == 'open_google':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Run google.exe'])
        play("test")

    elif cmd == 'music':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Run music.exe'])
        play("test")

    elif cmd == 'music_off':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Stop music.exe'])
        time.sleep(0.2)
        play("test")

    elif cmd == 'music_save':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Save music.exe'])
        time.sleep(0.2)
        play("test")

    elif cmd == 'music_next':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Next music.exe'])
        time.sleep(0.2)
        play("test")

    elif cmd == 'music_prev':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Prev music.exe'])
        time.sleep(0.2)
        play("test")

    elif cmd == 'sound_off':
        play("test", True)#ok
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)

    elif cmd == 'sound_on':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        play("test")# ready

    elif cmd == 'thanks':
        play("test")

    elif cmd == 'stupid':
        play("test")

    elif cmd == 'gaming_mode_on':
        play("test")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch to gaming mode.exe'])
        play("test")# ready

    elif cmd == 'gaming_mode_off':
        play("test")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch back to workspace.exe'])
        play("test")#ready

    elif cmd == 'switch_to_headphones':
        play("test")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch to headphones.exe'])
        time.sleep(0.5)
        play("test")#ready

    elif cmd == 'switch_to_dynamics':
        play("test")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch to dynamics.exe'])
        time.sleep(0.5)
        play("test")# ready

    elif cmd == 'off':
        play("off", True)

        exit(0)

    # elif cmd == 'soft_restart':
    #     play("off", True)
    #     porcupine.delete()
    #     python = sys.executable
    #     os.execl(python, python, *sys.argv)

    # elif cmd == 'hard_restart':
    #     play("off", True)
    #     os.system("shutdown /r /t 0")
    
    # elif cmd == 'off_system':
    #     play("off", True)
    #     os.system("shutdown /s /t 0")


def process_command(cmd):
    cmd = cmd.lower()# Приводим к нижнему регистру для унификации

    if "завершить процесс" in cmd:
        print("👋 ")
        print({"message": "Завершение работы по команде 'пока'."} )
        tts.va_speak("Выполняю протокол завершения работы")
        pause(1)  # Пауза для завершения речи
        exit(0)
        

    elif "привет" in cmd:
        print("👋 Привет! Как я могу помочь?")
        tts.va_speak("Привет! Как я могу помочь?")
        pause(1)  # Пауза для завершения речи

    elif "включи свет" in cmd:
        print("💡 Команда: включить свет")
        tts.va_speak("Включаю свет.")
        pause(1) # Пауза для завершения речи

    elif "открой окно" in cmd:
        print("🪟 Команда: открыть окно")
        tts.va_speak("Открываю окно.")
        pause(1)  # Пауза для завершения речи

    else:
        print(f"🤖 Неизвестная команда: {cmd}")
        tts.va_speak(f"неизвестная команда")
        pause(1)  # Пауза для завершения речи
        return False
    
    return True

SILENCE_TIMEOUT = 10  # секунд
last_voice_time = time.time() - 1000  # Инициализируем таймер в прошлом, чтобы сразу начать распознавание
if __name__ == "__main__":

    print("🎤 Готов к работе!")

    while True:
        
        try:
            print("🔊 Ожидание активации...")
            attemps = 0
            

            if  recognize_wake_up():
                last_voice_time = time.time()
                print("🟢 Активация: Да, сэр!")
                last_voice_time = time.time()  # Таймер для отслеживания тишины

                while (time.time() - last_voice_time <= SILENCE_TIMEOUT):
                    

                        text = recognize_continuous()

                        if not text.strip():
                            continue
                        last_voice_time = time.time() #обновляем таймер на звук
                        print(f"📥 Получено: {text}")
                        # Разбиваем на фразы-предложения
                        commands = [cmd.strip() for cmd in re.split(r'\s+затем\s+|\s+после\s+|\s+и\s+|[.,;!?]', text) if cmd.strip()]  # используем text, а не cmd

                        for cmd in commands:
                            print(f"Обработка команды: {cmd}")
                            cmd = cmd.lower()  # Приводим к нижнему регистру для унификации
                            pause(0.1)

                            if not process_command(cmd):
                                attemps += 1
                        if attemps >= 2:
                            break
                                
                        
                    
        except ValueError or Exception as err:
            print("\n⛔ Прервано аварийно:\n")
            print(f"Unexpected {err=}, {type(err)=}")
            raise
                    