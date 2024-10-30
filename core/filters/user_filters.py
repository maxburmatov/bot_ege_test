from aiogram.filters import BaseFilter
from aiogram.types import Message
from core.config_data.config import config

admin_ids = config.bots.admin_id

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in admin_ids