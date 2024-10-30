__all__ = ("router",)

from aiogram import Router

from core.handlers.user_handlers.callback_handlers.backpack_plagination import router as backpack_pagination_router
from core.handlers.user_handlers.callback_handlers.shop_cases import router as shop_cases_router
from core.handlers.user_handlers.callback_handlers.quests_plagination import router as quests_pagination_router

router = Router(name=__name__)

router.include_routers(
    backpack_pagination_router,
    shop_cases_router,
    quests_pagination_router
)