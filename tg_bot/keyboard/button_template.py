start_kb = [
    ("👑 VIP", "vip_panel"),
    ("🤝 Сотрудничество — партнерские программы и предложения", "cooperation_company"),
    ("ℹ️ О компании / Контакты", "about_company"),
]

# Админская часть
admin_keyboard = [
    ("📬 Создать рассылку", "broadcast_message"),
    ("🧑‍💼 Сотрудничество: новые заявки", "show_requests_cooperation"),
    ("🔍 Найти ID пользователя по username", "get_user_id_by_username"),
    ("🛡️ Назначить администратора", "add_admin"),
    ("🚫 Убрать права администратора", "remove_admin"),
    ("➕ Добавить группу в подписку", "add_group_to_subscription"),
    ("➖ Удалить группу с подписок", "remove_group_with_subscriptions"),
    ("📋 Список групп", "list_group"),
]

SPOT_COIN = [
    # Основные криптовалюты (с картинок + добавленные)
    "BTC", "ETH", "BNB", "SOL",
    "XRP", "ADA", "DOGE", "SHIB",
    "AVAX", "TRX", "DOT", "LINK",
    "NEAR", "MATIC", "LTC", "UNI",
    "PEPE", "TON", "BCH", "SUI",

    # DeFi токены
    "INJ", "CRV", "ONDO", "MNT",

    # Дополнительные популярные спотовые пары
    "ATOM", "FIL", "ETC", "XLM",
    "ALGO", "XTZ", "EOS", "AAVE",
    "COMP", "MKR", "SNX", "YFI",
    "SAND", "MANA", "ENJ", "CHZ",
    "VET", "THETA", "FTM", "ONE",
    "EGLD", "ZIL", "IOTA", "NEO",

    # Мем-коины
    "FLOKI", "BONK",

    # Layer 2 и новые проекты
    "ARB", "OP", "METIS", "IMX",
    "APT", "SEI", "TIA", "PYTH"
]

cancel_newsletter = [
    ("⏪ Отмена", 'cancel_newsletter')
]

cancel_cooperation = [
    ("⏪ Отмена", 'cancel_cooperation')
]

referral_system = [
    ("🎁 Реферальная система", "referral_system"),
]

buy_vip_kb = [
    ("💎 Приобрести VIP", "buy_vip_panel"),
]

select_vip_functions = [
    ("🔥 Лучшее предложение на SPOT", "weekend_spot"),
    ("📊 Актуальные SPOT-цены на всех биржах", "all_prices_spot"),
]


def get_accept_cancel_buttons(request_id: int):
    return [
        ("❌ Отклонить", f"cancel_cooperation_requests_{request_id}"),
        ("✅ Одобрить", f"accepted_cooperation_requests_{request_id}"),
        ("⏪ Отмена", "show_requests_cooperation_2")
    ]


def subscription_keyboard(prices):
    return [
        (f'🔔 {value["label"]}', plan.name) for plan, value in prices.items()
    ]
