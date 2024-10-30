__all__ = ("router",)

from aiogram import Router
from core.handlers.user_handlers.other_module import router as other_module_router
from core.handlers.user_handlers.solve_module import router as solve_module_router
from core.handlers.user_handlers.callback_handlers import router as callback_user_router

router = Router(name=__name__)

router.include_routers(
    other_module_router,
    callback_user_router,
    solve_module_router
)