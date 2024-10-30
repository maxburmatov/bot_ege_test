import asyncio
import logging
from aiogram.filters import CommandStart, Command
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from core.keyboards.main_menu import set_main_menu
from core.scheduler.main_scheduler import scheduler_start
from core.services.payment import pre_checkout_query, successful_pay
from database.create_database import db_start
from aiogram.enums import ContentType
from aiogram.enums.parse_mode import ParseMode

from config_data.config import config

from core import router as main_router

async def start_bot(bot: Bot):
    await db_start()
    await bot.send_message(config.bots.admin_id[0], text='Бот запущен!')

async def stop_bot(bot: Bot):
    await bot.send_message(config.bots.admin_id[0], text='Бот остановлен!')

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s.%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=config.bots.bot_token)

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_pay, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.startup.register(start_bot)
    dp.startup.register(set_main_menu)
    dp.shutdown.register(stop_bot)
    await scheduler_start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start())