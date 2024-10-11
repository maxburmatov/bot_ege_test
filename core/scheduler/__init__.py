__all__ = ("router",)

from aiogram import Router, Dispatcher, BaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from core.config_data.config import config

from core.handlers import router as handlers_router
from core.scheduler.update import update_league

router = Router(name=__name__)
dp = Dispatcher()

class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self,handler,event,data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)

async def scheduler_start():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware(
            SchedulerMiddleware(scheduler=scheduler),
        )
    scheduler.add_job(update_league, 'cron', hour=18, minute=19, second=0, kwargs={'bot': Bot})


#scheduler.add_job(reset_daily_stats, 'cron', hour=0, minute=0, second=0)
#scheduler.add_job(reset_weekly_var, 'cron', day_of_week='sun', hour=0, minute=0, second=5)
#scheduler.add_job(reset_month_points, 'cron', day=1, hour=0, minute=0, second=10)
#scheduler.add_job(send_message_reminder, 'interval', days=3, start_date='2023-11-20 16:00:00', kwargs={'bot': Bot})