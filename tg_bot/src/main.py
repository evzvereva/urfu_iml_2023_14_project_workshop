import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import Config, load_config
from handler import bot_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    config: Config = load_config()

    bot = Bot(token=config.tg_bot_config.token,
              parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)

    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(bot_router)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
