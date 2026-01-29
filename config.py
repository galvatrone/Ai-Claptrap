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

# External AI API configuration
AI_API_URL = os.getenv("AI_API_URL")
AI_API_TOKEN = os.getenv("AI_API_TOKEN")
AI_API_TIMEOUT = float(os.getenv("AI_API_TIMEOUT", "20"))
AI_API_REQUEST_FIELD = os.getenv("AI_API_REQUEST_FIELD", "prompt")
AI_API_RESPONSE_FIELD = os.getenv("AI_API_RESPONSE_FIELD", "response")
AI_API_AUTH_HEADER = os.getenv("AI_API_AUTH_HEADER", "Authorization")
AI_API_TOKEN_PREFIX = os.getenv("AI_API_TOKEN_PREFIX", "Bearer")
