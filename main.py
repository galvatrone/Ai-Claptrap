from stt.recognize import  recognize_continuous , recognize_wake_up


import tts


import queue
import re
import time
from time import sleep as pause


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




def process_command(cmd):
    cmd = cmd.lower()

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

if __name__ == "__main__":

    print("🎤 Готов к работе!")

    while True:
        
        try:
            print("🔊 Ожидание активации...")
            attemps = 0
            last_voice_time = time.time()  # Таймер для отслеживания тишины

            if  recognize_wake_up():
                last_voice_time = time.time()
                print("🟢 Активация: Да, сэр!")

                while True:
                    
                        # ждем новую команду из очереди с таймаутом, чтобы можно было реагировать
                        pause(0.5)  # небольшая пауза для снижения нагрузки
                        if time.time() - last_voice_time > SILENCE_TIMEOUT:
                            print("⏱", SILENCE_TIMEOUT, "секунд. Завершаем.")
                            break

                        text = recognize_continuous()
                        print("🧪 Говорится:", text)
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
                                if attemps >= 3:
                                    break
                                
                        
                    
        except ValueError or Exception as err:
            print("\n⛔ Прервано аварийно:\n")
            print(f"Unexpected {err=}, {type(err)=}")
            raise
                    