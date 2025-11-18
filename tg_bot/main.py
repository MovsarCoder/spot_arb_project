import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommandScopeAllPrivateChats

from config.settings import BotToken
from handlers import router
from tg_bot.keyboard.default_keyboard import commands
from tg_bot.middlewares.check_subscription_on_groups import SubscriptionMiddleware
from tg_bot.middlewares.logging import ErrorMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


async def main():
    bot = Bot(token=BotToken.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Подключение всех роутеров
    dp.include_router(router)

    # Удаление всех старый вебхуков
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Подключение базовой менюшки со всеми командами
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())

    # Подключение middleware на перехват всех ошибок и перенаправление их к администраторам
    dp.update.middleware(ErrorMiddleware())
    # Подключение middleware на проверку подписок на все каналы перед обрабатываем любых событий.
    dp.message.middleware(SubscriptionMiddleware())

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except TelegramBadRequest as e:
        logging.error(f"Telegram API error: {e}")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}", exc_info=True)
