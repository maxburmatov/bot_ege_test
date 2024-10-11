from aiogram.utils.keyboard import InlineKeyboardBuilder

async def payment_keyboard(stars):
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Заплатить {stars}⭐️", pay=True)
    return builder.as_markup()