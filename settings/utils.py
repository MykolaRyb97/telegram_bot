import logging
from pathlib import Path
import sys

def get_logger(name: str) -> logging.Logger:

    log_dir = Path(__file__).resolve().parent.parent / 'logs'
    log_file = log_dir / 'bot.log'


    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"Помилка доступу до директорії логів: {e}", file=sys.stderr)
        return logging.getLogger(name)  # Повертаємо базовий логгер без файлу


    logger = logging.getLogger(name)
    if not logger.handlers:  # Перевіряємо, чи вже є обробники

        logger.setLevel(logging.DEBUG)  # Змінили з INFO на DEBUG для кращого відстеження


        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Помилка створення file_handler: {e}", file=sys.stderr)


        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


        logger.propagate = False

    return logger