from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto

from core.database.admin_metods import get_request, \
    request_add_answer, request_mark_spam, request_mark_finished
from core.database.metods.get_student import get_name
from core.filters.user_filters import IsAdmin
from core.keyboards.inline_request_admin import get_type_requests_keyboard, RequestCallback, RequestType, RequestStatus, \
    RequestAction, get_requests_keyboard

from core.keyboards.reply_admin import get_admin_request_keyboard, \
    back_admin_request
from core.lexicon.lexicon import LEXICON_BUTTON, LEXICON_MEDIA
from core.states.states import StateAdminRequestAnswer
from core.utils.functions import delete_message

router = Router()

@router.message((F.text.startswith(f'{LEXICON_BUTTON["admin_request"]}')) | (F.text == LEXICON_BUTTON["back_admin_request"]), IsAdmin())
async def send_echo(message: Message):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Выбери нужное действие!", reply_markup=await get_admin_request_keyboard())


@router.message(F.text.startswith(f'{LEXICON_BUTTON["admin_new_request"]}'), IsAdmin())
async def send_echo(message: Message, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Новые обращения", reply_markup=back_admin_request)

    keyboard = await get_type_requests_keyboard(status_request="new")  # Page: 0
    path = LEXICON_MEDIA["category_request"]
    image = FSInputFile(path)
    caption = f"🤖: Выбери нужную категорию!"

    await bot.send_photo(
        photo=image,
        caption=caption,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )


@router.callback_query(
    RequestCallback.filter((F.type_request == RequestType.error) | (F.type_request == RequestType.question) | (F.type_request == RequestType.error_task)),
    RequestCallback.filter(F.status == RequestStatus.new),
    RequestCallback.filter(F.action == RequestAction.choose),
    IsAdmin()
)
async def backpack_page_handler(query: CallbackQuery, callback_data: RequestCallback):
    page = int(callback_data.page)

    info_request = await get_request(page, callback_data.status, callback_data.type_request)
    name_user = await get_name(info_request["tg_id"])
    keyboard = await get_requests_keyboard(page, info_request.get("count_requests"), callback_data.status, callback_data.type_request)

    caption = (f"Обращение #{info_request["id"]}\n"
               f"Дата обращения: {info_request["date_request"]}\n"
               f"TG_ID: {info_request["tg_id"]}\n"
               f"Имя: {name_user}\n\n"
               f"Текст обращения:\n"
               f"{info_request["text_request"]}\n\n"
               f"Ответ:\n"
               f"{info_request["answer_request"]}")

    photo = InputMediaPhoto(media=info_request["photo_request"], caption=caption)

    await query.message.edit_media(photo, reply_markup=keyboard)

@router.callback_query(
    RequestCallback.filter((F.type_request == RequestType.error) | (F.type_request == RequestType.question) | (F.type_request == RequestType.error_task)),
    RequestCallback.filter(F.status == RequestStatus.new),
    RequestCallback.filter(F.action == RequestAction.answer_user),
    IsAdmin()
)
async def backpack_page_handler1111(query: CallbackQuery, callback_data: RequestCallback, state: FSMContext):

    await state.update_data(page=callback_data.page)
    await state.update_data(status=callback_data.status)
    await state.update_data(type_request=callback_data.type_request)

    await query.message.answer("🤖: Ответ пользователю:")

    await state.set_state(StateAdminRequestAnswer.REQUEST_ANSWER)


@router.message(
    StateFilter(StateAdminRequestAnswer.REQUEST_ANSWER), IsAdmin()
)
async def request_answer12(message:Message, state: FSMContext, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    data = await state.get_data()
    answer_user = message.text

    info_request = await get_request(data.get("page"), data.get("status"), data.get("type_request"))
    name_user = await get_name(info_request["tg_id"])

    await request_add_answer(info_request["id"], answer_user)
    await message.answer(f"🤖: Ответ пользователю {name_user} отправлен!")

    answer_request = "🤖: Тебе пришел ответ от моих разработчиков по поводу твоего обращения:\n\n"
    answer_request += f"<blockquote>{answer_user}</blockquote>"

    await bot.send_message(
        text=answer_request,
        chat_id=info_request["tg_id"],
        parse_mode='HTML'
    )

    keyboard = await get_requests_keyboard(data.get("page"), info_request.get("count_requests"), data.get("status"),
                                           data.get("type_request"))
    caption = (f"Обращение #{info_request["id"]}\n"
               f"Дата обращения: {info_request["date_request"]}\n"
               f"TG_ID: {info_request["tg_id"]}\n"
               f"Имя: {name_user}\n\n"
               f"Текст обращения:\n"
               f"{info_request["text_request"]}\n\n"
               f"Ответ:\n"
               f"{answer_user}")

    image = info_request["photo_request"]

    await bot.send_photo(
        photo=image,
        caption=caption,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )

    await state.clear()


@router.callback_query(
    RequestCallback.filter((F.type_request == RequestType.error) | (F.type_request == RequestType.question) | (F.type_request == RequestType.error_task)),
    RequestCallback.filter(F.status == RequestStatus.new),
    RequestCallback.filter(F.action == RequestAction.mark_spam),
    IsAdmin()
)
async def backpack_page_handler1111(query: CallbackQuery, callback_data: RequestCallback, bot: Bot):

    info_request = await get_request(callback_data.page, callback_data.status, callback_data.type_request)

    await request_mark_spam(info_request["id"])

    answer_request = "🤖: Тебе пришло предупреждение от моих разработчиков по поводу твоего обращения:\n\n"
    answer_request += (f"<blockquote>Добрый день, мы не можем ответить на твое обращение и оно "
                       f"было отмечено как спам, так как в нем отсутствует конструктивная информация. "
                       f"Пожалуйста, пиши обращения только в случае необходимости или мы будем вынуждены "
                       f"ограничить тебе доступ к боту!</blockquote>")

    await bot.send_message(
        text=answer_request,
        chat_id=info_request["tg_id"],
        parse_mode='HTML'
    )

    await query.answer("🤖: Сообщение помечено как спам!")

    info_request = await get_request(callback_data.page, callback_data.status, callback_data.type_request)
    name_user = await get_name(info_request["tg_id"])

    keyboard = await get_requests_keyboard(callback_data.page, info_request.get("count_requests"), callback_data.status,
                                           callback_data.type_request)
    caption = (f"Обращение #{info_request["id"]}\n"
               f"Дата обращения: {info_request["date_request"]}\n"
               f"TG_ID: {info_request["tg_id"]}\n"
               f"Имя: {name_user}\n\n"
               f"Текст обращения:\n"
               f"{info_request["text_request"]}\n\n"
               f"Ответ:\n"
               f"{info_request["answer_request"]}")

    photo = InputMediaPhoto(media=info_request["photo_request"], caption=caption)
    await query.message.edit_media(photo, reply_markup=keyboard)

@router.callback_query(
    RequestCallback.filter((F.type_request == RequestType.error) | (F.type_request == RequestType.question) | (F.type_request == RequestType.error_task)),
    RequestCallback.filter(F.status == RequestStatus.new),
    RequestCallback.filter(F.action == RequestAction.mark_finished),
    IsAdmin()
)
async def backpack_page_handler1111(query: CallbackQuery, callback_data: RequestCallback):
    info_request = await get_request(callback_data.page, callback_data.status, callback_data.type_request)

    await request_mark_finished(info_request["id"])

    await query.answer("🤖: Сообщение помечено как прочитанное!")

    info_request = await get_request(callback_data.page, callback_data.status, callback_data.type_request)
    name_user = await get_name(info_request["tg_id"])

    keyboard = await get_requests_keyboard(callback_data.page, info_request.get("count_requests"), callback_data.status,
                                           callback_data.type_request)

    caption = (f"Обращение #{info_request["id"]}\n"
               f"Дата обращения: {info_request["date_request"]}\n"
               f"TG_ID: {info_request["tg_id"]}\n"
               f"Имя: {name_user}\n\n"
               f"Текст обращения:\n"
               f"{info_request["text_request"]}\n\n"
               f"Ответ:\n"
               f"{info_request["answer_request"]}")

    photo = InputMediaPhoto(media=info_request["photo_request"], caption=caption)
    await query.message.edit_media(photo, reply_markup=keyboard)


@router.callback_query(
    RequestCallback.filter(F.action == RequestAction.main),
    RequestCallback.filter(F.status == RequestStatus.new),
    IsAdmin()
)
async def backpack_page_handler(query: CallbackQuery):

    await query.answer("🤖: Новые обращения")

    keyboard = await get_type_requests_keyboard(status_request="new")  # Page: 0
    path = LEXICON_MEDIA["category_request"]
    image = FSInputFile(path)
    caption = f"🤖: Выбери нужную категорию!"

    photo = InputMediaPhoto(media=image, caption=caption)
    await query.message.edit_media(photo, reply_markup=keyboard)


@router.message(F.text.startswith(f'{LEXICON_BUTTON["admin_finished_request"]}'), IsAdmin())
async def send_echo(message: Message, bot: Bot):

    await delete_message(message, message.chat.id, message.message_id)

    await message.answer("🤖: Завершенные обращения", reply_markup=back_admin_request)

    keyboard = await get_type_requests_keyboard(status_request="finished")  # Page: 0
    path = LEXICON_MEDIA["category_request"]
    image = FSInputFile(path)
    caption = f"🤖: Выбери нужную категорию!"

    await bot.send_photo(
        photo=image,
        caption=caption,
        chat_id=message.chat.id,
        reply_markup=keyboard
    )

@router.callback_query(
    RequestCallback.filter((F.type_request == RequestType.error) | (F.type_request == RequestType.question) | (F.type_request == RequestType.error_task)),
    RequestCallback.filter(F.status == RequestStatus.finished),
    RequestCallback.filter(F.action == RequestAction.choose),
    IsAdmin()
)
async def backpack_page_handler(query: CallbackQuery, callback_data: RequestCallback):
    page = int(callback_data.page)

    info_request = await get_request(page, callback_data.status, callback_data.type_request)
    name_user = await get_name(info_request["tg_id"])
    keyboard = await get_requests_keyboard(page, info_request.get("count_requests"), callback_data.status, callback_data.type_request)

    caption = (f"Обращение #{info_request["id"]}\n"
               f"Дата обращения: {info_request["date_request"]}\n"
               f"TG_ID: {info_request["tg_id"]}\n"
               f"Имя: {name_user}\n\n"
               f"Текст обращения:\n"
               f"{info_request["text_request"]}\n\n"
               f"Ответ:\n"
               f"{info_request["answer_request"]}\n\n"
               f"Комментарий:\n"
               f"{info_request["comment_request"]}")

    photo = InputMediaPhoto(media=info_request["photo_request"], caption=caption)

    await query.message.edit_media(photo, reply_markup=keyboard)

@router.callback_query(
    RequestCallback.filter(F.action == RequestAction.main),
    RequestCallback.filter(F.status == RequestStatus.finished),
    IsAdmin()
)
async def backpack_page_handler(query: CallbackQuery):

    await query.answer("🤖: Завершенные обращения")

    keyboard = await get_type_requests_keyboard(status_request="finished")  # Page: 0
    path = LEXICON_MEDIA["category_request"]
    image = FSInputFile(path)
    caption = f"🤖: Выбери нужную категорию!"

    photo = InputMediaPhoto(media=image, caption=caption)
    await query.message.edit_media(photo, reply_markup=keyboard)