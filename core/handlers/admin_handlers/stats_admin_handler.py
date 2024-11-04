from datetime import date

from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from aiogram.utils.deep_linking import create_start_link
from core.database.admin_metods import admin_add_task_database, get_task_info, admin_edit_task_database, \
    get_general_daily_stats
from core.database.metods.get_student import get_count_invite, get_daily_temp
from core.database.metods.quests import generate_daily_quests
from core.filters.user_filters import IsAdmin

from core.keyboards.reply_admin import get_admin_panel, admin_edit_menu, main_menu_keyboard_admin, back_admin_panel
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.services.admin_create_image_task import create_image_task
from core.states.states import StateAdminAddTask, StateAdminEditTask
from core.utils.functions import delete_message

router = Router()

@router.message(F.text == LEXICON_BUTTON["admin_stats"],
                IsAdmin()
                )
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    date_today = str(date.today())

    stats_dict = await get_general_daily_stats()

    text_info = (f"Дата: {date_today}\n\n"
                 
                 f"[Пользователи]\n\n"
                 f"Новые: +{stats_dict["count_new_students"]}\n"
                 f"Всего: {stats_dict["count_all_students"]}\n"
                 f"Активные: {stats_dict["count_daily_active_students"]}\n"
                 f"% активных пользователей: {stats_dict["percent_active_daily_students"]}\n\n"
                 
                 f"[Решено]\n\n"
                 f"Всего заданий: {stats_dict["count_tasks"]}\n"
                 f"Всего тестов: {stats_dict["count_tests"]}\n"
                 f"Всего вариантов: {stats_dict["count_variants"]}\n"
                 f"Всего заданий дня: {stats_dict["count_daily_task"]}\n"
                 f"% решений заданий дня: {stats_dict["percent_count_daily_task"]}\n\n"
                 
                 f"[Баллы]\n\n"
                 f"Всего баллов: {stats_dict["sum_points"]}\n"
                 f"Ср. кол-во баллов: {int(stats_dict["avg_points"])}\n"
                 f"Максимум баллов: {stats_dict["max_points"]}\n"
                 f"Лидер дня: ({stats_dict["leader_name"]}, {stats_dict["leader_title_league"]}, {stats_dict["leader_tg_id"]})\n\n"
                 
                 f"[Квесты]\n\n"
                 f"Выполнено всего: *OTDELRAZRABOTKI-23*\n"
                 f"Остальные всего: *OTDELRAZRABOTKI-23*\n"
                 f"Ежедневные всего: {stats_dict["count_completed_daily_quests"]}\n"
                 f"Выполнены все еж. квесты: {stats_dict["count_completed_all_daily_quests"]}\n"
                 f"% выполнения всех еж. квестов: {stats_dict["percent_completed_all_daily_quests"]}\n\n"
                 
                 f"[Кейсы]\n\n"
                 f"Получено: *OTDELRAZRABOTKI-27*\n"
                 f"Куплено: *OTDELRAZRABOTKI-25*\n\n"
                 
                 f"[Подписка]\n\n"
                 f"Оформлено: *OTDELRAZRABOTKI-25*\n"
                 f"Интересовались: *OTDELRAZRABOTKI-26*\n"
                 f"% интересовавшихся: -\n\n"
                 
                 f"[Заработано]\n\n"
                 f"Кейсы: *OTDELRAZRABOTKI-25*\n"
                 f"Подписки: *OTDELRAZRABOTKI-25*\n"
                 f"Всего: -\n"

                 )

    await message.answer(text_info, reply_markup=back_admin_panel)