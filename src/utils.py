import logging

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')


    file_handler = logging.FileHandler('bot.log', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Помилки та вищі рівні в консоль
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
