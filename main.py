from stt.recognize import  recognize_continuous , recognize_wake_up

import random
import tts

import config
import queue
import re
import time
from time import sleep as pause
import os

import yaml
from fuzzywuzzy import fuzz
import torch
import subprocess
import requests

import simpleaudio as sa

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from colorama import init, Fore, Style
init(autoreset=True)



 
 # в будущем можно будет сделать несколько потоков для распознавания речи и обработки команд 
 # чем больше потоков тем больше нагрузка на процессор и память
 # больше пользователей говорят одновремено то больше потоков распознавания разношо голоса 
os.environ['VOSK_LOG_LEVEL'] = '0'
print("Загрузка TTS модели...")
model = torch.hub.load('snakers4/silero-models', 'silero_tts', language='ru')
 # или 'cuda', если есть GPU
print("Модель загружена и готова к работе.")

CDIR = os.path.dirname(os.path.abspath(__file__))  # Получаем текущую директорию

VA_CMD_LIST = yaml.safe_load(
    open(os.path.join(CDIR, 'commands.yaml'), 'rt', encoding='utf8'),
)

def build_ai_headers():
    headers = {"Content-Type": "application/json"}
    if config.AI_API_TOKEN:
        token = config.AI_API_TOKEN
        if config.AI_API_TOKEN_PREFIX:
            token = f"{config.AI_API_TOKEN_PREFIX} {token}"
        headers[config.AI_API_AUTH_HEADER] = token
    return headers


def call_ai_api(prompt: str):
    if not config.AI_API_URL:
        print("AI API URL not configured (AI_API_URL).")
        return None

    try:
        resp = requests.post(
            config.AI_API_URL,
            json={config.AI_API_REQUEST_FIELD: prompt},
            headers=build_ai_headers(),
            timeout=config.AI_API_TIMEOUT,
        )
        resp.raise_for_status()
    except Exception as exc:
        print(f"AI API request failed: {exc}")
        return None

    try:
        data = resp.json()
    except ValueError:
        return resp.text.strip() if resp.text else None

    if isinstance(data, dict):
        if config.AI_API_RESPONSE_FIELD in data:
            return data[config.AI_API_RESPONSE_FIELD]
        for key in ("text", "response", "reply", "answer", "result", "message", "текст", "ответ", "сообщение", "результат"):
            if key in data:
                return data[key]

    if isinstance(data, str):
        return data

    return None


def extract_ai_query(raw_voice: str):
    if not raw_voice:
        return ""

    voice = raw_voice.strip()
    for prefix in VA_CMD_LIST.get("ai", []):
        if voice.startswith(prefix):
            return voice[len(prefix):].strip(" ,.!?;:")
    return voice



def play(phrase, wait_done=True):
    """
    Воспроизводит .wav файл из папки sound/ по ключевому слову phrase.
    
    :param phrase: имя файла без расширения (.wav добавляется автоматически)
    :param wait_done: True — ждать окончания воспроизведения
    """
    global recorder

    # Собираем путь к файлу .wav
    filename = os.path.join(CDIR, "sound", phrase + ".wav")

    # Проверяем, существует ли файл
    if not os.path.isfile(filename):
        print(f"⚠️ Файл не найден: {filename}")
        return

    try:
        # Останавливаем запись перед воспроизведением (если нужно)
        # if wait_done and recorder:
        #     recorder.stop()

        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()

        if wait_done:
            play_obj.wait_done()
            # recorder.start()

    except Exception as e:
        print(f"⛔ Error run: {e}")




def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd

def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            if c == "ai" and cmd.startswith(x):
                return {'cmd': c, 'percent': 100}
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc




def execute_cmd(cmd: str, voice: str):

    if cmd == 'open_browser':
        subprocess.Popen([f'{CDIR}\\custom-commands\\Run browser.exe'])
        play("OVER HERE PT2")

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
        play("stay-dead-dipshit", True)#ok
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)

    elif cmd == 'sound_on':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        play("DEFEND YOU")# ready

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
        play("DON'T WORRY BABY")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch to headphones.exe'])
        time.sleep(0.5)
        play("OVER HERE PT2")

    elif cmd == 'switch_to_dynamics':
        play("DON'T WORRY BABY")
        subprocess.check_call([f'{CDIR}\\custom-commands\\Switch to dynamics.exe'])
        time.sleep(0.5)
        play("OVER HERE PT2")

    elif cmd == 'off_assistant':
        play("I'M GOING TO DIE", True)
        exit(0)
    elif cmd == 'ai':
        query = extract_ai_query(voice)
        if not query:
            play("I GOT NOTHING")
            return False

        response = call_ai_api(query)
        if response:
            tts.va_speak(str(response))
        else:
            play("I GOT NOTHING")
    else :
        play("I GOT NOTHING")
        # tts.va_speak(f"неизвестная команда")
        pause(1)  # Пауза для завершения речи
        return False
    return True
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

SILENCE_TIMEOUT = 10  # секунд
last_voice_time = time.time() - 1000  # Инициализируем таймер в прошлом, чтобы сразу начать распознавание
if __name__ == "__main__":

    print("Ready to Work!")
    play("Hello")  # Воспроизводим приветствие
    while True:
        
        try:
            print("waiting for activation...")
            attemps = 0
            
            fail = False
            if  recognize_wake_up():
                last_voice_time = time.time()
                print(f"{Fore.YELLOW} Activation: Yes, sir!{Style.RESET_ALL}")
                play("understant")
                last_voice_time = time.time()  # Таймер для отслеживания тишины

                while (time.time() - last_voice_time <= SILENCE_TIMEOUT):
                    

                        text = recognize_continuous()

                        if not text.strip():
                            continue
                        last_voice_time = time.time() #обновляем таймер на звук
                        # print(f"📥 Получено: {text}")
                        # Разбиваем на фразы-предложения
                        commands = [cmd.strip() for cmd in re.split(r'\s+затем\s+|\s+после\s+|\s+и\s+|[.,;!?]', text) if cmd.strip()]  # используем text, а не cmd

                        for cmd in commands:
                            raw_cmd = cmd.lower()# Приводим к нижнему регистру для унификации
                            print(f"processing: {raw_cmd}")  
                            pause(0.1)
                            cmd = recognize_cmd(filter_cmd(raw_cmd))
                            # print(cmd)
                            cmd_obj = {'cmd': cmd['cmd'], 'percent': cmd['percent']}

                            print(f"{Fore.GREEN}command processing:{Style.RESET_ALL} {Fore.CYAN}{cmd_obj['cmd']}{Style.RESET_ALL} | percent: {Fore.MAGENTA}{cmd_obj['percent']}%{Style.RESET_ALL}")
                            if cmd_obj['percent'] > 70:
                                    fail=execute_cmd(cmd['cmd'],raw_cmd)
                            else:
                                attemps += 1
                            if fail:
                                attemps += 1
                        if attemps >= 2:
                            break
                                
                        
                    
        except ValueError or Exception as err:
            print("\n⛔ interrupted emergency:\n")
            print(f"Unexpected {err=}, {type(err)=}")
            #log.error(f"Unexpected {err=}, {type(err)=}")

            raise
                    
