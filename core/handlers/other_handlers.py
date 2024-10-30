from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.reply import main_menu, main_menu_keyboard
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_COMMANDS
from aiogram.filters import CommandStart, Command
from core.utils.functions import delete_message

router = Router(name=__name__)


@router.message((F.text == LEXICON_BUTTON["back_menu"]) | (F.text == "/menu")
                )
async def send_echo(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await state.clear()
    await bot.send_sticker(message.from_user.id,
                           "CAACAgIAAxkBAAJShWU8wyWkZ6vYvm3qKHDWmwhsghZ5AAI0DAAC6QiISlc3ARD4weYnMAQ")
    await message.answer("🤖: Выбери нужный раздел!", reply_markup=await main_menu_keyboard())


@router.message()
async def send_echo(message: Message):
    await message.answer(f'Это сообщение не обработано нужным хэндлером!')
