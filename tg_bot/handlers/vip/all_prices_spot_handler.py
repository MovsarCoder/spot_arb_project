from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup,
    KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext

from tg_bot.keyboard.button_template import SPOT_COIN
from tg_bot.states.state import GetCointNameStates
from parser.parser_merge import parser_merge

import html

router = Router()


# ----------------------- UTILS -----------------------

def chunk_list(lst, size=3):
    """Разбить список на части по size"""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def generate_keyboard_with_coins():
    rows = chunk_list(SPOT_COIN, 3)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=c) for c in row] for row in rows],
        resize_keyboard=True
    )


def fmt(num):
    try:
        return f"{float(num):.10f}"
    except Exception:
        return html.escape(str(num))


def generate_update_keyboard(coin):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Лучшее предложение на SPOT", callback_data="weekend_spot")],
        [InlineKeyboardButton(text="🔄 Обновить цену", callback_data=f"update_price:{coin}")],
        [InlineKeyboardButton(text="🆕 Новый коин", callback_data="new_coint")],
    ])


def format_result_text_html(data: dict) -> str:
    """
    Форматирует данные по биржам в HTML для Telegram.
    Поддерживает словари с ключами 'symbol' и 'price_usdt',
    а также None или нестандартные данные.
    """
    parts = ""

    for exchange, d in data.items():
        exch = html.escape(str(exchange))

        if isinstance(d, dict):
            symbol = html.escape(str(d.get("symbol", "—")))
            price_usdt = fmt(d.get("price_usdt", "—"))

            block = (
                f"<b>🏦 Биржа:</b> <code>{exch}</code>\n\n"
                f"  💵  <b>{symbol}/USDT: </b> <code>{price_usdt}</code>\n\n"
                f"<i>{'—' * 30}</i>\n\n"
            )
        elif d is not None:
            # Если данные есть, но не словарь
            block = (
                f"<b>🏦 Биржа:</b> <code>{exch}</code>\n\n"
                f"  💵  {html.escape(str(d))}\n\n"
                f"<i>{'—' * 30}</i>\n\n"
            )
        else:
            # Если данных нет
            block = (
                f"<b>🏦 Биржа:</b> <code>{exch}</code>\n\n"
                f"<b>❗️ Пара не торгуется на бирже!</b>\n\n"
                f"<i>{'—' * 30}</i>\n\n"
            )

        parts += block

    return parts


async def send_loading(message: Message):
    """Показать индикатор загрузки и вернуть объект сообщения"""
    return await message.answer("⏳ Подождите, получаем данные...")


# ----------------------- ROUTES -----------------------

@router.callback_query(F.data == 'all_prices_spot')
async def all_prices_spot(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        "Выберите коин 👇",
        reply_markup=generate_keyboard_with_coins()
    )
    await state.set_state(GetCointNameStates.get_name_coint)


@router.message(GetCointNameStates.get_name_coint, F.text.in_(SPOT_COIN))
async def get_coin(message: Message, state: FSMContext):
    coin = message.text.strip().lower()
    loading_msg = await send_loading(message)
    data = await parser_merge(coin)
    await loading_msg.delete()

    if not data:
        await message.answer("❌ Ошибка получения цены.")
        return

    await message.answer(
        format_result_text_html(data),
        reply_markup=generate_update_keyboard(coin)
    )
    await state.clear()


@router.message(GetCointNameStates.get_name_coint)
async def invalid_coin(message: Message):
    await message.answer(
        "⚠️ Выберите коин из списка!",
        reply_markup=generate_keyboard_with_coins()
    )


@router.callback_query(F.data.startswith("update_price:"))
async def refresh_price(callback: CallbackQuery, state: FSMContext):
    coin = callback.data.split(":")[1]
    loading_msg = await send_loading(callback.message)
    data = await parser_merge(coin)
    await loading_msg.delete()

    if not data:
        await callback.answer("❌ Ошибка обновления!", show_alert=True)
        return

    new_text = format_result_text_html(data)

    if callback.message.text == new_text:
        await callback.answer("🔄 Цена уже актуальная!")
        return

    await callback.message.edit_text(
        new_text,
        reply_markup=generate_update_keyboard(coin)
    )
    await callback.answer("🔄 Обновлено!")
    await state.clear()


@router.callback_query(F.data == "new_coint")
async def new_coint(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выберите новый коин 👇",
        reply_markup=generate_keyboard_with_coins()
    )
    await state.set_state(GetCointNameStates.get_name_coint)
