from aiogram import Router, Bot, F
from aiogram.types import Message

from aiogram.utils.deep_linking import create_start_link
from core.database.metods.get_student import get_count_invite

from core.keyboards.reply import info_menu, main_menu
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS

router = Router()