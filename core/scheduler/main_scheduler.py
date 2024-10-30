from aiogram import Router, Dispatcher, BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from core.scheduler.update import update_league
from core.utils.functions import generate_date_update_league
from core.scheduler.daily_reset import reset_daily_stats
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
    #timezone='Europe/Moscow'
    scheduler = AsyncIOScheduler()
    scheduler.start()
    dp.update.middleware(
            SchedulerMiddleware(scheduler=scheduler),
        )
    list_date, last_day_date = await generate_date_update_league()
    scheduler.add_job(update_league, 'cron', hour=17, minute=43, second=0, kwargs={'bot': Bot})
    scheduler.add_job(reset_daily_stats, 'cron', hour=0, minute=31, second=0)


#scheduler.add_job(reset_daily_stats, 'cron', hour=0, minute=0, second=0)
#scheduler.add_job(reset_weekly_var, 'cron', day_of_week='sun', hour=0, minute=0, second=5)
#scheduler.add_job(reset_month_points, 'cron', day=1, hour=0, minute=0, second=10)
#scheduler.add_job(send_message_reminder, 'interval', days=3, start_date='2023-11-20 16:00:00', kwargs={'bot': Bot})