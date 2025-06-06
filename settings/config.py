
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseSettings):
    OPENAI_API_KEY: str
    TOKEN_TELEGRAM_API: str

    openai_model: str = 'gpt-3.5-turbo'
    openai_model_temperature: float = 0.7  # 0 - 2.0

    path_to_images: Path = BASE_DIR / 'resources' / 'images'
    path_to_messages: Path = BASE_DIR / 'resources' / 'messages'
    path_to_prompts: Path = BASE_DIR / 'resources' / 'prompts'
    path_to_logs: Path = BASE_DIR / 'logs'

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / '.env'),
        env_file_encoding='utf-8',
        extra='ignore'
    )

try:
    config = AppConfig()
except Exception as e:
    print(f"Error loading config: {e}")
    raise