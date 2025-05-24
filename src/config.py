
import os
from pathlib import Path


BASE_DIR = Path('C:/Users/User/Desktop/Навчання/telegram_bot_final_project_1')
env_file = BASE_DIR / '.env'


if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

TELEGRAM_BOT_API_KEY = os.environ.get('TELEGRAM_BOT_API_KEY')
OPENAI_API_TOKEN = os.environ.get('OPENAI_API_KEY')

def get_responses_main(path_file: str):
    with open(path_file, encoding='utf-8') as file:
        return file.read()
    

