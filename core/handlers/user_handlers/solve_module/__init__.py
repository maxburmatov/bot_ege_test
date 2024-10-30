__all__ = ("router",)

from aiogram import Router
from core.handlers.user_handlers.solve_module.general_solve_handler import router as general_solve_router
from core.handlers.user_handlers.solve_module.random_task_handler import router as random_task_router
from core.handlers.user_handlers.solve_module.specific_task_handler import router as specific_task_router
from core.handlers.user_handlers.solve_module.test_tasks_handler import router as test_tasks_router
from core.handlers.user_handlers.solve_module.daily_task_handler import router as daily_task_router

router = Router(name=__name__)

router.include_routers(
    general_solve_router,
    random_task_router,
    specific_task_router,
    test_tasks_router,
    daily_task_router
)