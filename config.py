"""
Конфигурация бота
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Путь к проекту
BASE_DIR = Path(__file__).parent

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', '')

# ID модератора в Telegram
MODERATOR_ID = int(os.getenv('MODERATOR_ID', '0'))

# Email настройки
EMAIL_TO = os.getenv('EMAIL_TO', '')
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

# Канал для проверки подписки
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME', '')

# Путь к структуре бота
BOT_STRUCTURE_FILE = BASE_DIR / 'bot_structure.json'

# Путь для сохранения ответов
RESPONSES_DIR = BASE_DIR / 'responses'

# Проверка обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")

if not MODERATOR_ID:
    raise ValueError("MODERATOR_ID не установлен в .env файле")

