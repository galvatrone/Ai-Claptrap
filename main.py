from stt.recognize import  recognize_continuous , recognize_wake_up


import tts


import queue
import re
import time
from time import sleep as pause
import os

import yaml
from fuzzywuzzy import fuzz
import torch



 
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
def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in VA_CMD_LIST.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt
    return rc


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
                    