from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tg_bot.keyboard.keyboard_builder import make_row_inline_keyboards
from tg_bot.keyboard.button_template import admin_keyboard

from database.crud import CrudUser

router = Router()


@router.message(Command('admin_panel'))
async def admin_panel_command(message: Message, state: FSMContext):
    await state.clear()

    admins = await CrudUser().check_is_admin_user()
    people_id = message.from_user.id

    if people_id not in admins:
        await message.answer(f"{message.from_user.username}({people_id}), простите. Но, вам не доступны админские функции!")
        return

    await message.answer(
        "Добро пожаловать в админ панель!",
        reply_markup=make_row_inline_keyboards(admin_keyboard)
    )
