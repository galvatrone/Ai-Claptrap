from stt.recognize import  recognize_continuous 

import tts

import threading
import queue
import time
import re

results_queue = queue.Queue()

import torch

 # Загрузка модели TTS сперва
 # исправить настройки модели, если нужно
 # исправить второй поток что бы активировался stt только после активации tss
 # разобрать в паралельных потоков а пока больше потоков не создавать, а использовать один для распознавания речи
 # в будущем можно будет сделать несколько потоков для распознавания речи и обработки команд 
 # чем больше потоков тем больше нагрузка на процессор и память
 # больше пользователей говорят одновремено то больше потоков распознавания разношо голоса 

print("Загрузка TTS модели...")
model = torch.hub.load('snakers4/silero-models', 'silero_tts', language='ru')
 # или 'cuda', если есть GPU
print("Модель загружена и готова к работе.")


def recognize_background():

    while True:
        text = recognize_continuous()  # твоя функция блокирует пока не получит результат
        results_queue.put(text)
        if "пока" in text.lower():
            break

thread = threading.Thread(target=recognize_background)
thread.daemon = True
thread.start()

def process_command(cmd):
    cmd = cmd.lower()

    if "пока" in cmd:
        print("⛔ Завершаем")
        tts.va_speak("До свидания!")
        

    elif "привет" in cmd:
        print("👋 Привет! Как я могу помочь?")
        tts.va_speak("Привет! Как я могу помочь?")

    elif "включи свет" in cmd:
        print("💡 Команда: включить свет")
        tts.va_speak("Включаю свет.")

    elif "открой окно" in cmd:
        print("🪟 Команда: открыть окно")
        tts.va_speak("Открываю окно.")

    else:
        print(f"🤖 Неизвестная команда: {cmd}")
        tts.va_speak(f"Вы сказали: {cmd}")
    
    return True

if __name__ == "__main__":
    
    print("🎤 Готов к работе! Говорите 'привет' для активации.")
    while True:
        try:
            # ждем новую команду из очереди с таймаутом, чтобы можно было реагировать
            text = results_queue.get(timeout=0.5)  # здесь переменная должна называться text, а не cmd

        except queue.Empty:
            continue
        
        if not text.strip():
            continue
        print(f"📥 Получено: {text}")
        # Разбиваем на фразы-предложения
        commands = [cmd.strip() for cmd in re.split(r'\s+затем\s+|\s+после\s+|\s+и\s+|[.,;!?]', text) if cmd.strip()]  # используем text, а не cmd

        for cmd in commands:
            print(f"Обработка команды: {cmd}")
            cmd = cmd.lower()  # Приводим к нижнему регистру для унификации
            if not process_command(cmd):
                exit()
