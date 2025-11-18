import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from tg_bot.keyboard.keyboard_builder import make_row_inline_keyboards
from tg_bot.keyboard.button_template import start_kb
from tg_bot.config.settings import GetBotName
from database.crud import CrudUser

router = Router()

BOT_NAME = GetBotName.BOT_NAME

HTML_WELCOME = f"""<b>⚡ Добро пожаловать в спотовый арбитраж {BOT_NAME}⚡️</b>

<i>🔍 Мы помогаем находить лучшие возможности для заработка на разнице цен между биржами.</i>

<b>Больше не нужно вручную сравнивать стоимость монет — наш сервис делает это за вас.</b>

<b>Что вы получите:</b>
• 💹 <b>Умный поиск арбитражных связок</b>
 — мгновенно находим, где монету <i>купить дешевле</i>, а где — <i>продать дороже</i>.
• 📉 <b>Анализ цен на десятках площадок</b>
 — сравнение крупнейших бирж и подбор лучших точек входа/выхода.
• ⚙️ <b>Автоматизация процесса</b>
 — сокращаем ручную работу и ускоряем принятие решений.
• 🚀 <b>Максимизация прибыли</b>
 — инструменты для заработка даже на небольших расхождениях цен.
 
<b>Для теста вам был выдан 1 день бесплатного использования VIP-функций! Не упустите шанс подзаработать!</b>

<b>Как начать:</b>
1) Нажмите кнопку «VIP» в списке ниже 👇.
2) Выберите монету и биржи для сравнения.
3) Получите список выгодных пар и рекомендации по ордерам.

"""


def extract_referred_id(payload: str | None) -> int | None:
    """
    Извлекает telegram_id пригласившего из payload, если он есть.
    """
    if payload and payload.startswith("ref_"):
        try:
            return int(payload.removeprefix("ref_"))
        except (IndexError, ValueError):
            pass
    return None


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, command: CommandObject):
    """
    Обработка команды /start. Регистрирует пользователя, проверяет реферала.
    """
    await state.clear()

    referred_by_telegram_id = extract_referred_id(command.args)
    crud = CrudUser()

    try:
        user = await crud.add_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            firstname=message.from_user.first_name,
            lastname=message.from_user.last_name,
            is_admin=False,
            referred_by_telegram_id=referred_by_telegram_id,
        )
        if user:
            logging.info(f"✅ Пользователь {user.telegram_id} успешно зарегистрирован.")
        else:
            logging.info(f"👤 Пользователь {message.from_user.id} уже существует.")
    except Exception as e:
        logging.error(f"❌ Ошибка при добавлении пользователя {message.from_user.id}: {e}", exc_info=True)

    await message.answer(
        text=HTML_WELCOME,
        reply_markup=make_row_inline_keyboards(start_kb),
    )
