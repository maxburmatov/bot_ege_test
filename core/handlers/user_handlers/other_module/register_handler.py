import asyncio

from aiogram import Router, Bot, F

from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.payload import decode_payload
from core.database.metods.register_student import check_add_student, add_student
from core.database.metods.get_student import get_name
from core.keyboards.reply import choose_purpose_menu, back_menu, main_menu
from core.states.states import StateRegisterUser

from core.lexicon.lexicon import LEXICON, LEXICON_BUTTON

router = Router(name=__name__)

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, command: Command, bot: Bot):
    await state.update_data(invite_tg_id=await check_invited(command.args))

    if await check_add_student(message.from_user.id):
        await new_student_message(message.from_user.id, message.from_user.first_name, bot)
        await state.set_state(StateRegisterUser.IDENT_PURPOSE)
    else:
        await old_student_message(message.from_user.id, bot)

@router.message(
    (StateFilter(StateRegisterUser.IDENT_PURPOSE)), ((F.text == LEXICON_BUTTON["purpose_1"]) | (F.text == LEXICON_BUTTON["purpose_2"]) | (F.text == LEXICON_BUTTON["purpose_3"]) | (F.text == LEXICON_BUTTON["purpose_4"]))
)
async def process_ident_purpose(message: Message, state: FSMContext, bot: Bot):

    answer_user = message.text
    data = await state.get_data()
    invite_tg_id = data['invite_tg_id']

    match answer_user:
        case "до 70 баллов":
            purpose = 1
        case "70-85 баллов":
            purpose = 2
        case "85-95 баллов":
            purpose = 3
        case "95+ баллов":
            purpose = 4
        case _:
            purpose = 0

    await send_info_invite(invite_tg_id, message.from_user.first_name, bot)
    await add_student(message.from_user.id, message.from_user.first_name, purpose, invite_tg_id)
    await message.answer("🤖: Отлично! Теперь ты можешь начинать! Если что, цель по баллам можно "
                         "поменять в любой момент в своем профиле.", reply_markup=back_menu)
    await state.clear()

@router.message(StateFilter(StateRegisterUser.IDENT_PURPOSE))
async def process_ident_purpose(message: Message, state: FSMContext, bot: Bot):
    await message.answer("🤖: Нажми на кнопку с желаемым количеством баллов!", reply_markup=choose_purpose_menu)
    await state.set_state(StateRegisterUser.IDENT_PURPOSE)

async def check_invited(command_args):
    if command_args is not None:
        args = command_args
        invite_tg_id = decode_payload(args)
        return invite_tg_id

async def send_info_invite(invite_tg_id, name_friend, bot: Bot):
    if invite_tg_id is not None:
        await bot.send_message(invite_tg_id, f"🤖: Ты пригласил друга: {name_friend}! Готовтесь вместе!")

async def old_student_message(tg_id, bot: Bot):
    await bot.send_sticker(tg_id,"CAACAgIAAxkBAAJSUWU8qHpCzGN_-v73X6wiyVBck6EEAAIBAAMWbkwSH3u_BkTp24swBA")
    await bot.send_chat_action(tg_id, action="typing")
    await asyncio.sleep(2)
    await bot.send_message(tg_id, f"🤖: Рад снова тебя видеть, {await get_name(tg_id)}!"
                         f" С чего начнем?", reply_markup=main_menu)
async def new_student_message(tg_id, name, bot: Bot):
    await bot.send_message(tg_id, f"🤖: Приветствую, {name}!"
                                  f" Я учебный бот-тренажер! Я помогу тебе подготовиться к ЕГЭ по математике!")
    await bot.send_chat_action(tg_id, action="typing")
    await asyncio.sleep(5)
    await bot.send_message(tg_id, f"🤖: Со мной ты сможешь отточить свои навыки до идеала!"
                         f" Здесь можно тренироваться решать задания определенного номера, проходить тесты по заданиям для закрепления,"
                         f" прорешивать целые варианты из заданий первой части!")
    await bot.send_chat_action(tg_id, action="typing")
    await asyncio.sleep(10)
    await bot.send_message(tg_id, f"🤖: НО! Чтобы тебе было интереснее я сделал соревновательную и немножко игровую систему."
                         f" За правильное и быстрое выполнение заданий я буду начислять тебе баллы, в ином случае забирать обратно."
                         f" Чтобы заработать дополнительные баллы, я буду подкидывать тебе ежедневные и еженедельные задания.")
    await bot.send_chat_action(tg_id, action="typing")
    await asyncio.sleep(10)
    await bot.send_message(tg_id,
        f"🤖: Чем больше баллов у тебя будет, тем выше будет твой рейтинг. В конце каждого месяца лучшие ученики получат от меня подарочки!"
        f" Брось вызов своим друзьям или одноклассникам, ну или просто соревнуйся с другими ребятами!")
    await bot.send_chat_action(tg_id, action="typing")
    await asyncio.sleep(8)
    await bot.send_message(tg_id, f"🤖: А теперь пора переходить к делу!"
                         f" Давай определимся на какие баллы ты планируешь сдать ЕГЭ. Выбери желаемое количество баллов!",
                         reply_markup=choose_purpose_menu)
