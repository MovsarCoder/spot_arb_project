import requests

# -------------------------------
# 1. Получаем список всех спотовых пар с USDT
# -------------------------------
KUCOIN_SYMBOLS_URL = "https://api.kucoin.com/api/v1/symbols"
KUCOIN_TICKER_URL = "https://api.kucoin.com/api/v1/market/orderbook/level1"


def get_spot_usdt_symbols():
    resp = requests.get(KUCOIN_SYMBOLS_URL)
    resp.raise_for_status()
    data = resp.json()["data"]

    symbols = []
    for s in data:
        if s["quoteCurrency"] == "USDT" and s["enableTrading"]:
            symbols.append(s["symbol"])
    return symbols


# -------------------------------
# 2. Получаем цену крипты в USDT
# -------------------------------
def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    spot_symbols = get_spot_usdt_symbols()

    # Найдём правильную пару
    pair_usdt = f"{symbol}-USDT"
    if pair_usdt not in spot_symbols:
        return False

    resp = requests.get(KUCOIN_TICKER_URL, params={"symbol": pair_usdt})
    resp.raise_for_status()
    data = resp.json()["data"]
    price_usdt = float(data["price"])

    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }


# -------------------------------
# 3. ТЕСТ
# -------------------------------
if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    result = get_crypto_price_in_usdt(coin)

    if isinstance(result, dict):
        print(f"{result['symbol']}/USDT = {result['price_usdt']} USDT")
    else:
        print("Пара не найдена на KuCoin")
