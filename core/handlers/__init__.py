__all__ = ("router",)

from aiogram import Router

from core.handlers.user_handlers import router as user_handlers_router
from core.handlers.admin_handlers import router as admin_handlers_router
from core.handlers.private_user_handlers import router as private_user_handlers_router
from core.handlers.other_handlers import router as other_handlers_router

# from core.handlers.user_handlers.register_handler import router as register_handler_router

router = Router(name=__name__)

router.include_routers(
    user_handlers_router,
    admin_handlers_router,
    private_user_handlers_router
)

router.include_routers(other_handlers_router)
