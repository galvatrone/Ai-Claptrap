import datetime
import json
import os
import queue
import random
import struct
import subprocess
import sys
import time
from ctypes import POINTER, cast


import openai
from openai import OpenAI


import pvporcupine
import simpleaudio as sa
import vosk
import yaml
from comtypes import CLSCTX_ALL
from fuzzywuzzy import fuzz
from pvrecorder import PvRecorder
from pycaw.pycaw import (
    AudioUtilities,
    IAudioEndpointVolume
)
from rich import print

import config
import tts

# # some consts
CDIR = os.getcwd()
CDIR = os.path.dirname(os.path.abspath(__file__))

VA_CMD_LIST = yaml.safe_load(
    open(os.path.join(CDIR, 'commands.yaml'), 'rt', encoding='utf8'),
)

# # ChatGPT vars
# system_message = {"role": "system", "content": "Ты голосовой ассистент из железного человека."}
# message_log = [system_message]




# try:
#     porcupine = pvporcupine.create(
#         access_key=config.PICOVOICE_TOKEN,
#         keywords=['jarvis', 'bumblebee', 'computer'],
#         sensitivities=[1, 0.9, 0.95]

#     )
# except Exception as e:
#     print("Ошибка при инициализации Porcupine:", e)
#     exit(1)


# VOSK
try:
    model = vosk.Model("model_small")
except Exception as e:
    print("Ошибка при загрузке модели Vosk:", e)
    exit(1)

samplerate = 16000
device = config.MICROPHONE_INDEX
kaldi_rec = vosk.KaldiRecognizer(model, samplerate)
q = queue.Queue()

# Создаём клиента один раз, желательно в глобальной области
# try:
#     client = OpenAI(api_key=config.OPENAI_TOKEN)
# except Exception as e:
#     print("Ошибка при инициализации OpenAI:", e)
#     exit(1)


#################################################################
# import traceback

# def gpt_answer():
#     global message_log
#     model_engine = "gpt-3.5-turbo"
#     max_tokens = 256

#     try:
#         response = client.chat.completions.create(
#             model=model_engine,
#             messages=message_log,
#             max_tokens=max_tokens,
#             temperature=0.7,
#             top_p=1,
#         )

#         # Проверка на пустой ответ
#         if not response.choices or not response.choices[0].message.content:
#             return "Извините, я не смог придумать ответ."

#         return response.choices[0].message.content.strip()

#     except Exception as ex:
#         print(f"Произошла Generateees ошибка API:\n{type(ex).__name__}: {ex}\n\n{traceback.format_exc()}")
#         return f" Gemerate voice ХУЙ Произошла ошибка: {ex}"
################################################################################### 


def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def va_respond(voice: str):
    global recorder, message_log
    print(f"Распознано: {voice}")

    cmd = recognize_cmd(filter_cmd(voice))

    print(cmd)

    if len(cmd['cmd'].strip()) <= 0:
        return False
    elif cmd['percent'] < 70 or cmd['cmd'] not in VA_CMD_LIST.keys():
        if fuzz.ratio(voice.join(voice.split()[:1]).strip(), "скажи") > 75:
            message_log.append({"role": "user", "content": voice})
            response = gpt_answer()
            message_log.append({"role": "assistant", "content": response})
            recorder.stop()
            tts.va_speak(response)
            time.sleep(0.5)
            recorder.start()
            return False
        else:
            play("not_found")
            time.sleep(1)

        return False
    else:
        execute_cmd(cmd['cmd'], voice)
        return True


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
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc



try:
    recorder = PvRecorder(device_index=config.MICROPHONE_INDEX, frame_length=porcupine.frame_length)
    recorder.start()
except Exception as e:
    print(f"Ошибка при создании/запуске рекордера: {e}")
    exit(1)


# print('Using device: %s' % recorder.selected_device)

print(f"Инициализация голосового ассистента...Прототип Железяки (V 0.0.1)")
print(f"Используемое устройство: {recorder.selected_device.name}")
print(f"Выбранный микрофон: {config.MICROPHONE_INDEX}")
# print(f"Porcupine frame length: {porcupine.frame_length}")

# try:
#     play("run")
# except Exception as e:
#     print(f"Ошибка при воспроизведении 'run': {e}")

time.sleep(0.5)

ltc = time.time() - 1000

while True:
    try:
        
        pcm = recorder.read()
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            recorder.stop()
            play("greet", True)
            print("Yes, sir.")
            recorder.start()
            ltc = time.time()

        while time.time() - ltc <= 10:
            pcm = recorder.read()
            sp = struct.pack("h" * len(pcm), *pcm)

            if kaldi_rec.AcceptWaveform(sp):
                if va_respond(json.loads(kaldi_rec.Result())["text"]):
                    ltc = time.time()
                break

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
