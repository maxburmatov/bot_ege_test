from aiogram import F, Router, Bot

from core.database.metods.shop import get_shop_case
from core.keyboards.inline_payment import payment_keyboard
from core.keyboards.inline_shop import get_shop_cases_keyboard, CasesCallback, ShopActions, BuyItemsCount

from aiogram.types import CallbackQuery, InputMediaPhoto, LabeledPrice


router = Router()


# noinspection PyTypeChecker
@router.callback_query(CasesCallback.filter(F.action == ShopActions.choose))
async def cases_page_handler(query: CallbackQuery, callback_data: CasesCallback, bot: Bot):
    page = int(callback_data.page)
    count_cases, info_case = await get_shop_case(page)
    cases_data = info_case["cases_data"]
    case = cases_data[0]
    title_case = case[1]
    image_case = case[3]

    print(case)
    caption = f"Ты выбрал: {title_case}"
    keyboard = await get_shop_cases_keyboard(page)

    photo = InputMediaPhoto(media=image_case, caption=caption)

    await query.message.edit_media(photo, reply_markup=keyboard)

@router.callback_query(CasesCallback.filter(F.action == ShopActions.buy),
                       CasesCallback.filter(F.item_count == BuyItemsCount.one))
async def shop_buy_case(query: CallbackQuery, callback_data: CasesCallback, bot: Bot):
    page = int(callback_data.page)
    count_cases, info_case = await get_shop_case(page)
    cases_data = info_case["cases_data"]
    case = cases_data[0]

    title = case[1]
    display_name = case[2]
    payload = case[5]
    image = case[3]
    price = case[4]

    PRICE = LabeledPrice(label=title, amount=price)

    await bot.send_invoice(
        chat_id=query.from_user.id,
        title=display_name,
        description=f"Оплата заказа",
        provider_token="",
        payload=payload,
        currency="XTR",
        prices=[PRICE],
        photo_url=image,
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_size=512,
        reply_markup=await payment_keyboard(price),
    )


@router.callback_query(CasesCallback.filter(F.action == ShopActions.buy),
                       CasesCallback.filter(F.item_count == BuyItemsCount.five))
async def shop_buy_case(query: CallbackQuery, callback_data: CasesCallback, bot: Bot):
    page = int(callback_data.page)
    count_cases, info_case = await get_shop_case(page)
    cases_data = info_case["cases_data"]
    case = cases_data[1]

    title = case[1]
    display_name = case[2]
    payload = case[5]
    image = case[3]
    price = case[4]

    PRICE = LabeledPrice(label=title, amount=price)

    await bot.send_invoice(
        chat_id=query.from_user.id,
        title=display_name,
        description=f"Оплата заказа",
        provider_token="",
        payload=payload,
        currency="XTR",
        prices=[PRICE],
        photo_url=image,
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_size=512,
        reply_markup=await payment_keyboard(price),
    )


@router.callback_query(CasesCallback.filter(F.action == ShopActions.buy),
                       CasesCallback.filter(F.item_count == BuyItemsCount.twenty))
async def shop_buy_case(query: CallbackQuery, callback_data: CasesCallback, bot: Bot):
    page = int(callback_data.page)
    count_cases, info_case = await get_shop_case(page)
    cases_data = info_case["cases_data"]
    case = cases_data[2]

    title = case[1]
    display_name = case[2]
    payload = case[5]
    image = case[3]
    price = case[4]

    PRICE = LabeledPrice(label=title, amount=price)

    await bot.send_invoice(
        chat_id=query.from_user.id,
        title=display_name,
        description=f"Оплата заказа",
        provider_token="",
        payload=payload,
        currency="XTR",
        prices=[PRICE],
        photo_url=image,
        photo_height=512,  # !=0/None, иначе изображение не покажется
        photo_width=512,
        photo_size=512,
        reply_markup=await payment_keyboard(price),
    )

