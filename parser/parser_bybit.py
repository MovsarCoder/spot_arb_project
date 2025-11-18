import requests

# ===============================
#   1. Получение цен крипты (Bybit)
# ===============================

def get_tickers(category="linear"):
    """Получаем все tickers для линейных фьючерсов"""
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": category}
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    data = resp.json()
    if data["retCode"] != 0:
        raise Exception(f"Ошибка API Bybit: {data}")

    return data["result"]["list"]


def get_symbol_price(symbol: str, tickers: list):
    """Находим цену пары (например BTCUSDT)"""
    symbol = symbol.upper()
    for t in tickers:
        if t["symbol"] == symbol:
            return float(t["lastPrice"])
    return None


# ===============================
#   2. Главная функция
# ===============================

def get_crypto_price_in_usdt(base_symbol: str):
    """
    Возвращает цену крипты в USDT
    """

    tickers = get_tickers()
    pair = f"{base_symbol.upper()}USDT"

    price_usdt = get_symbol_price(pair, tickers)
    if price_usdt is None:
        return False

    return {
        "symbol": base_symbol.upper(),
        "price_usdt": price_usdt
    }


# ===============================
#   3. ТЕСТ
# ===============================

if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    result = get_crypto_price_in_usdt(coin)

    if isinstance(result, dict):
        print(f"{result['symbol']}/USDT = {result['price_usdt']:.4f} USDT")
    else:
        print(f"Пара {coin.upper()}USDT не найдена на Bybit")
