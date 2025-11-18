import os

from dotenv import load_dotenv

load_dotenv()


class BotToken:
    TOKEN: str
    TOKEN = os.getenv("BOT_TOKEN")


class GetBotName:
    BOT_NAME: str
    BOT_USERNAME: str

    BOT_NAME = os.getenv("BOT_NAME")
    BOT_USERNAME = os.getenv("BOT_USERNAME")


class YooKassaInfo:
    PAY_TOKEN: str
    SHOP_ID: int

    PAY_TOKEN = os.getenv("PAYMENT_TOKEN")
    SHOP_ID = os.getenv("SHOP_ID")
