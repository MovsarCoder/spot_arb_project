from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from tg_bot.keyboard.button_template import buy_vip_kb, select_vip_functions
from tg_bot.keyboard.keyboard_builder import make_row_inline_keyboards
from database.crud import CrudUser

router = Router()


async def open_vip_panel(message_or_callback, user_id, state: FSMContext):
    await state.clear()

    crud_user = CrudUser()
    user = await crud_user.get_user_by_id(user_id)

    now = datetime.now()
    has_active_subscription = any(
        sub.expires_at > now for sub in user.subscriptions
    )

    if not has_active_subscription:
        await message_or_callback.answer(
            "🚫 У вас нет доступа к VIP-функциям.\n"
            "Если вы хотите пользоваться расширенными возможностями — оформите VIP-подписку ниже 👇",
            reply_markup=make_row_inline_keyboards(buy_vip_kb)
        )
        return

    await message_or_callback.answer(
        "✨ Выберите необходимое действие из списка ниже:",
        reply_markup=make_row_inline_keyboards(select_vip_functions)
    )


@router.callback_query(F.data == "vip_panel")
async def vip_panel_callback_query(callback_query: CallbackQuery, state: FSMContext):
    await open_vip_panel(callback_query.message, callback_query.from_user.id, state)


@router.message(Command("vip"))
async def vip_panel_command(message: Message, state: FSMContext):
    await open_vip_panel(message, message.from_user.id, state)
