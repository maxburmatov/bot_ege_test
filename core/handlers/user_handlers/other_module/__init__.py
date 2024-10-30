__all__ = ("router",)

from aiogram import Router
from core.handlers.user_handlers.other_module.register_handler import router as register_handler_router
from core.handlers.user_handlers.other_module.room_handler import router as room_router
from core.handlers.user_handlers.other_module.table_leaders_handlers import router as table_leaders_router
from core.handlers.user_handlers.other_module.info_handlers import router as info_router
from core.handlers.user_handlers.other_module.shop_handler import router as shop_router
from core.handlers.user_handlers.other_module.quests_handlers import router as quests_router

router = Router(name=__name__)

router.include_routers(
    register_handler_router,
    shop_router,
    room_router,
    table_leaders_router,
    info_router,
    quests_router
)