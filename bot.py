import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from settings.config import config
from settings.utils import get_logger
from src.handlers import router

logger = get_logger(__name__)

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def main() -> None:
    try:
        bot = Bot(
            token=config.TOKEN_TELEGRAM_API,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        logger.info("Бот розпочав свою роботу...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Виникла помилка при старті: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())