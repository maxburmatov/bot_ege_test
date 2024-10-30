from aiogram import Router, Bot, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from aiogram.utils.deep_linking import create_start_link
from core.database.metods.get_student import get_count_invite
from core.database.metods.request_users import add_request

from core.keyboards.reply import info_menu, help_menu, back_info, faq_menu
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_STICKERS
from core.states.states import StateRequestError, StateRequestQuestion
from core.utils.functions import delete_message

router = Router()

@router.message((F.text == LEXICON_BUTTON["info"]) | (F.text == LEXICON_BUTTON["back_info"]) | (F.text == "/info"))
async def info(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await state.clear()

    await bot.send_sticker(message.from_user.id, LEXICON_STICKERS["info"])
    await message.answer("🤖: Что хочешь посмотреть?", reply_markup=info_menu)

@router.message(F.text == LEXICON_BUTTON["invite_friends"])
async def invite_friends(message: Message, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    count_invite_friends = await get_count_invite(message.from_user.id)
    answer_invite = await message_invite(count_invite_friends)

    await message.answer(f"🤖: Твоя ссылка для приглашений, нажми на нее и она скопируется:\n"
                         f"<code>{link}</code> "
                         f"\n\n{answer_invite}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=info_menu)


@router.message(F.text == LEXICON_BUTTON["help"])
async def invite_friends(message: Message, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Чем я могу помочь?",
                         reply_markup=help_menu)

@router.message(F.text == LEXICON_BUTTON["report_error"])
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Пожалуйста, подробно опиши в чём заключается ошибка, если нужно прикрепи скриншот!",
                         reply_markup=back_info)

    await state.set_state(StateRequestError.REQUEST_ERROR)


@router.message(StateFilter(StateRequestError.REQUEST_ERROR), F.content_type.in_({'text'}))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text_request = message.text
    date_request = message.date

    await add_request(date_request, message.chat.id, "error", text_request, None, "new")

    await message.answer(f"🤖: Благодарю за помощь! Сообщение об ошибке успешно отправлено, мои разработчики этим займутся!",
                         reply_markup=help_menu)

    await state.clear()

@router.message(StateFilter(StateRequestError.REQUEST_ERROR), F.content_type.in_({'photo'}))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text_request = message.caption
    photo_request = message.photo[-1].file_id
    date_request = message.date

    await add_request(date_request, message.chat.id, "error", text_request, photo_request, "new")

    await message.answer(f"🤖: Благодарю за помощь! Сообщение об ошибке успешно отправлено, мои разработчики этим займутся!",
                         reply_markup=help_menu)

    await state.clear()
@router.message(StateFilter(StateRequestError.REQUEST_ERROR))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Я тебя не понимаю... Отправь текстовое сообщение или сообщение со скриншотом!",
                         reply_markup=back_info)

    await state.set_state(StateRequestError.REQUEST_ERROR)


@router.message(F.text == LEXICON_BUTTON["faq"])
async def invite_friends(message: Message, bot: Bot, state: FSMContext):
    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: [Вопрос - Ответ]",
                         reply_markup=faq_menu)

@router.message(F.text == LEXICON_BUTTON["ask_question"])
async def invite_friends(message: Message, bot: Bot, state: FSMContext):
    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Здесь ты можешь задать любой свой вопрос, если нужно прикрепи скриншот!",
                         reply_markup=back_info)

    await state.set_state(StateRequestQuestion.REQUEST_QUESTION)


@router.message(StateFilter(StateRequestQuestion.REQUEST_QUESTION), F.content_type.in_({'text'}))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text_request = message.text
    date_request = message.date

    await add_request(date_request, message.chat.id, "question", text_request, None, "new")

    await message.answer(f"🤖: Я принял твой вопрос, уточню у разработчиков и вернусь к тебе с ответом!",
                         reply_markup=help_menu)

    await state.clear()

@router.message(StateFilter(StateRequestQuestion.REQUEST_QUESTION), F.content_type.in_({'photo'}))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    text_request = message.caption
    photo_request = message.photo[-1].file_id
    date_request = message.date

    await add_request(date_request, message.chat.id, "question", text_request, photo_request, "new")

    await message.answer(f"🤖: Я принял твой вопрос, уточню у разработчиков и вернусь к тебе с ответом!",
                         reply_markup=help_menu)

    await state.clear()
@router.message(StateFilter(StateRequestQuestion.REQUEST_QUESTION))
async def invite_friends(message: Message, bot: Bot, state: FSMContext):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer(f"🤖: Я тебя не понимаю... Отправь текстовое сообщение или сообщение со скриншотом!",
                         reply_markup=back_info)

    await state.set_state(StateRequestQuestion.REQUEST_QUESTION)


async def message_invite(count_invite_friends):
    if count_invite_friends == 0:
        str_invite = f"🤖: Пока что у тебя нет приглашений :("
    elif count_invite_friends < 5:
        str_invite = f"🤖: Ты пригласил {count_invite_friends} друга!"
    else:
        str_invite = f"🤖: Ты пригласил {count_invite_friends} друзей!"

    return str_invite
