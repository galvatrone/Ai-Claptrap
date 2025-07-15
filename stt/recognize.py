import queue # Очередь для асинхронной обработки аудио
import sounddevice as sd # Библиотека для работы с аудио
import vosk # Библиотека для распознавания речи
import json # Для работы с JSON-данными
import re # Регулярные выражения для обработки текста
import time # Для работы со временем

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from config import VA_ALIAS  # filepath: d:\Python\New-Voice\stt\recognize.py
VA_ALIAS_RU = ("приём",'железяка',"робот","жестянка","железный человек","железяка привет","клапт","клаптрап","клап трап")
VA_ALIAS_EN = ("nine","claptrap","clap-trap","ClapTrap","clap trap","jeleziaka","jelezo")


result_queue = queue.Queue()  # Очередь для результатов распознавания

def load_model(language_code):
    if language_code == "en":
        return vosk.Model("model_en")
    elif language_code == "ru":
        return vosk.Model("Vosk_models/Android/model_ru" or "model_ru_v3")
    elif language_code == "gr":
        return vosk.Model("model_gr")
    else:
        raise ValueError("Язык не поддерживается")

# language = input("🌐 Выберите язык (en/ru/de): ").strip().lower()

try:
    vosk_model = load_model("ru")
except Exception as e:
    print("Ошибка при загрузке модели Vosk:", e)
    exit(1)

q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print(status)
    q.put(bytes(indata))

def split_sentences(text):
    # Простая сегментация на предложения
    return re.findall(r'[^.!?]*[.!?]', text, re.DOTALL)

# def recognize():
#     print("🎤 Говорите... (нажмите Ctrl+C для остановки)")

#     with sd.RawInputStream(samplerate=16000, blocksize=8000,
#                            dtype='int16', channels=1, callback=callback):

#         rec = vosk.KaldiRecognizer(vosk_model, 16000)

        

#         is_active = False  # Ассистент "спит"
#         buffer = ""
#         full_text = ""
#         last_voice_time = time.time()  # Таймер для отслеживания тишины
#         try:
#             while True:
#                 data = q.get()
#                 if rec.AcceptWaveform(data):
#                     result = json.loads(rec.Result())
#                     part = result.get("text", "")

#                     if not is_active:
#                         continue  # Не активирован — игнорируем текст

#                     # Удаляем слово активации из начала распознанного текста
#                     for alias in VA_ALIAS_RU or VA_ALIAS_EN:
#                         if part.lower().startswith(alias):
#                             part = part[len(alias):].lstrip()
#                             break

#                     if part:

#                         part += "."
#                         buffer = " " + part

#                         # sentences = split_sentences(buffer)

#                         # for s in sentences[:-1]:
#                         #     s_clean = s.strip()
#                         #     if s_clean:
#                         #         print("📥 1Отправка в LLM:", s_clean)
#                         #         # process_with_llm(s_clean)
                                
#                         print("📥 Отправка в LLM:", part)
#                         return part.strip()
#                         # process_with_llm(s_clean)
#                         # buffer = sentences[-1] if sentences else ""
#                         full_text += " " + buffer.strip()

#                         print("📝 Остаток в буфере:", buffer.strip())
#                 else:
#                     partial = json.loads(rec.PartialResult()).get("partial", "")
#                     if not is_active:
#                         if any(word in partial.lower() for word in VA_ALIAS_RU or VA_ALIAS_EN):
#                             print("👂 Ключевое слово распознано — активация ассистента.")
#                             is_active = True
#                             partial= ""
#                             last_voice_time = time.time()
#                     else:
#                         if partial:
#                             last_voice_time = time.time()  # обновляем таймер на звук
#                             print("🧪 Говорится:", partial)

#                 # Проверка таймаута тишины
#                 if is_active and (time.time() - last_voice_time > SILENCE_TIMEOUT):
#                     print("⏱ Тишина больше", SILENCE_TIMEOUT, "секунд. Завершаем.")
#                     is_active = False
#                     buffer = ""
#                     print("📥 [ФИНАЛ] Отправка полного текста в LLM:", full_text.strip())
#                     return full_text.strip()
#                     full_text = ""
#                     #process_with_llm(full_text.strip())

#         except KeyboardInterrupt or ValueError or Exception as err:
#             print("\n⛔ Прервано аварийно:")
#             print(f"Unexpected {err=}, {type(err)=}")
#             if buffer:
#                 print("📥 [ФИНАЛ] Отправка остатка в LLM:", buffer.strip())
#                 # process_with_llm(buffer.strip())
#             raise


def recognize_wake_up():

    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                           dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(vosk_model, 16000)
        is_active=False
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    part = result.get("text", "")

                    if not is_active:
                        continue
                    else:
                        #
                        # if part:
                            # print("📥 Отправка монолога в LLM для обучения",part.strip())
                        return True
                else:
                    partial = json.loads(rec.PartialResult()).get("partial", "")
                    if not is_active:
                        if any(word in partial.lower() for word in VA_ALIAS_RU or VA_ALIAS_EN):
                            is_active=True

        except ValueError or Exception as err:
            print("\n⛔ Прервано аварийно:\n")
            print(f"Unexpected {err=}, {type(err)=}")
            raise




def recognize_continuous():
    with sd.RawInputStream(samplerate=16000, blocksize=8000,
                            dtype='int16', channels=1, callback=callback):

        rec = vosk.KaldiRecognizer(vosk_model, 16000)
        last_voice_time = time.time()  # Таймер для отслеживания тишины
        is_active = True  # Ассистент "активен"
        SILENCE_TIMEOUT = 10  # секунд

        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    part = result.get("text", "")

                    if not is_active:
                        continue

                    # Удаляем слово активации из начала распознанного текста
                    for alias in VA_ALIAS_RU or VA_ALIAS_EN:
                        if part.lower().startswith(alias):
                            part = part[len(alias):].lstrip()
                            break

                    if part:
                        part += "."
                          
                        # print("📥 Отправка в LLM:", part)
                        return part.strip()
                        # process_with_llm(part.strip())

                else:
                    partial = json.loads(rec.PartialResult()).get("partial", "")
                    if partial:
                        last_voice_time= time.time()  # обновляем таймер на звук
                        # print("🧪 Говорится:", partial)
                
                #                 # Проверка таймаута тишины
                if is_active and (time.time() - last_voice_time > SILENCE_TIMEOUT):
                    # print("⏱ Тишина больше", SILENCE_TIMEOUT, "секунд. Завершаем.")
                    is_active = False
                    # print("📥 [ФИНАЛ] Отправка полного текста в LLM:", part.strip())
                    return part.strip()
#                     #process_with_llm(full_text.strip())


        except KeyboardInterrupt or ValueError or Exception as err:
            print("\n⛔ Прервано аварийно:")
            print(f"Unexpected {err=}, {type(err)=}")
            if part:
                print("📥 [ФИНАЛ] Отправка остатка в LLM:", part.strip())
            # process_with_llm(buffer.strip())
            raise

