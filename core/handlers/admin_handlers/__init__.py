__all__ = ("router",)

from aiogram import Router
from core.handlers.admin_handlers.main_admin_handler import router as main_admin_router
from core.handlers.admin_handlers.edit_admin_handler import router as edit_admin_router
from core.handlers.admin_handlers.request_admin_handler import router as request_admin_router
from core.handlers.admin_handlers.stats_admin_handler import router as stats_admin_router

router = Router(name=__name__)

router.include_routers(
    main_admin_router,
    edit_admin_router,
    request_admin_router,
    stats_admin_router
)

