from dotenv import load_dotenv
import os

# Find .env file with os variables
load_dotenv("dev.env")

# Конфигурация
VA_NAME = 'Сlap-Trap'
VA_VER = "0.1"
VA_ALIAS_RU = ("приём",'железяка',"робот","жестянка","железный человек","железяка привет","клапт","клаптрап","клап трап")
VA_ALIAS_EN = ("nine","claptrap","clap-trap","ClapTrap","clap trap","jeleziaka","jelezo")
VA_ALIAS = VA_ALIAS_RU + VA_ALIAS_EN
VA_TBR = ('скажи', 'покажи', 'ответь', 'произнеси', 'расскажи', 'сколько', 'слушай')

# ID микрофона (можете просто менять ID пока при запуске не отобразится нужный)
# -1 это стандартное записывающее устройство
MICROPHONE_INDEX = -1

# # Путь к браузеру Google Chrome
# CHROME_PATH = 'C:/Users/micha/AppData/Local/Yandex/YandexBrowser/Application/browser.exe %s'



# # Токен PicovoicePICOVOICE_TOKEN=your_actual_access_key_here

# PICOVOICE_TOKEN = os.getenv('PICOVOICE_TOKEN')

# # Токен OpenAI
# OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
