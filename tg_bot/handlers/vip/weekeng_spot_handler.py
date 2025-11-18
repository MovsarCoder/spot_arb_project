from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, ReplyKeyboardMarkup, KeyboardButton,
    Message, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.context import FSMContext
from tg_bot.keyboard.button_template import SPOT_COIN
from tg_bot.states.state import GetCointNameStates
from parser.parser_merge import parser_merge
import html

router = Router()


# ------------------- UTILS -------------------

def chunk_list(lst, size=3):
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
        [InlineKeyboardButton(text="📊 Актуальные SPOT-цены на всех биржах", callback_data="all_prices_spot")],
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=f"update_weekend_price:{coin}")],
        [InlineKeyboardButton(text="🆕 Новый коин", callback_data="new_weekend_coint")],
    ])


async def send_loading(message: Message):
    return await message.answer("⏳ Подождите, получаем данные...")


# ------------------- BUSINESS LOGIC -------------------

def calculate_arbitrage(data: dict):
    # Берём только корректные данные
    prices_usdt = {
        exch: info.get("price_usdt")
        for exch, info in data.items()
        if info and isinstance(info, dict) and info.get("price_usdt") is not None
    }

    if not prices_usdt:
        return None

    min_exch = min(prices_usdt, key=prices_usdt.get)
    max_exch = max(prices_usdt, key=prices_usdt.get)
    buy_price = prices_usdt[min_exch]
    sell_price = prices_usdt[max_exch]

    profit = sell_price - buy_price
    profit_percent = (profit / buy_price) * 100 if buy_price else 0

    return {
        "buy_exch": min_exch,
        "sell_exch": max_exch,
        "buy_price": buy_price,
        "sell_price": sell_price,
        "profit": profit,
        "profit_percent": profit_percent
    }


def format_result_text_html(data: dict, arb: dict = None) -> str:
    if not data:
        return "Нет данных для отображения."

    first_info = next((info for info in data.values() if info and isinstance(info, dict)), None)
    symbol = html.escape(first_info.get('symbol', '—')) if first_info else "—"
    text = f"<b>🏖 Выгодный Спот: {symbol}</b>\n\n"

    min_price = arb["buy_price"] if arb else None
    max_price = arb["sell_price"] if arb else None

    for exch, info in data.items():
        if not info or not isinstance(info, dict):
            text += (
                f"<b>🏦 Биржа:</b> <code>{exch}</code>\n\n"
                f"<b>❗️ Пара не торгуется на бирже!</b>\n\n"
                f"<i>{'—' * 30}</i>\n\n"
            )
            continue

        price_usdt = info.get("price_usdt")
        arrow = ""
        if min_price is not None and price_usdt == min_price:
            arrow = "🔻"
        elif max_price is not None and price_usdt == max_price:
            arrow = "🔺"

        text += (
            f"🏦 <b>Биржа:</b> {html.escape(exch)}\n\n"
            f"  💵 <b>{info.get('symbol', '—')}/USDT</b>: <code>{fmt(price_usdt)}</code> {arrow}\n\n"
            f"<i>{'—' * 30}</i>\n\n"
        )

    if arb:
        text += (
            f"\n📈 <b>Где дешевле купить:</b> {html.escape(arb['buy_exch'])} за {fmt(arb['buy_price'])} USDT 🔻\n"
            f"📉 <b>Где дороже продать:</b> {html.escape(arb['sell_exch'])} за {fmt(arb['sell_price'])} USDT 🔺\n"
            f"💸 <b>Выгода:</b> {fmt(arb['profit'])} USDT ({fmt(arb['profit_percent'])}%)\n"
        )

    return text


# ------------------- ROUTES -------------------

@router.callback_query(F.data == 'weekend_spot')
async def weekend_spot(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        "Выберите коин для weekend 👇",
        reply_markup=generate_keyboard_with_coins()
    )
    await state.set_state(GetCointNameStates.get_name_coint_weekend)


@router.message(GetCointNameStates.get_name_coint_weekend, F.text.in_(SPOT_COIN))
async def get_coin_weekend(message: Message, state: FSMContext):
    coin = message.text.strip().lower()
    loading_msg = await send_loading(message)
    data = await parser_merge(coin)
    await loading_msg.delete()
    if not data:
        await message.answer("❌ Ошибка получения цены для weekend!")
        return
    arb = calculate_arbitrage(data)
    await message.answer(
        format_result_text_html(data, arb),
        reply_markup=generate_update_keyboard(coin)
    )
    await state.clear()


@router.message(GetCointNameStates.get_name_coint_weekend)
async def invalid_coin_weekend(message: Message):
    await message.answer(
        "⚠️ Выберите коин из списка для weekend!",
        reply_markup=generate_keyboard_with_coins()
    )


@router.callback_query(F.data.startswith("update_weekend_price:"))
async def refresh_weekend_price(callback: CallbackQuery, state: FSMContext):
    coin = callback.data.split(":")[1]
    loading_msg = await send_loading(callback.message)
    data = await parser_merge(coin)
    await loading_msg.delete()
    if not data:
        await callback.answer("❌ Ошибка обновления!", show_alert=True)
        return
    arb = calculate_arbitrage(data)
    new_text = format_result_text_html(data, arb)
    if callback.message.text == new_text:
        await callback.answer("🔄 Цена уже актуальна!")
        return
    await callback.message.edit_text(
        new_text,
        reply_markup=generate_update_keyboard(coin)
    )
    await callback.answer("🔄 Обновлено!")
    await state.clear()


@router.callback_query(F.data == "new_weekend_coint")
async def new_coint_weekend(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выберите новый коин для weekend 👇",
        reply_markup=generate_keyboard_with_coins()
    )
    await state.set_state(GetCointNameStates.get_name_coint_weekend)
