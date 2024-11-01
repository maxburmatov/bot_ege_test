__all__ = ("router",)

from aiogram import Router

from core.handlers import router as handlers_router


router = Router(name=__name__)

router.include_routers(
    handlers_router
)