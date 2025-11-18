import requests

BITGET_SYMBOLS_URL = "https://api.bitget.com/api/v2/spot/public/symbols"
BITGET_TICKERS_URL = "https://api.bitget.com/api/v2/spot/market/tickers"


# -------------------------------
#   Получаем список пар *крипта/USDT* (Bitget)
# -------------------------------
def get_spot_usdt_symbols():
    resp = requests.get(BITGET_SYMBOLS_URL)
    resp.raise_for_status()
    data = resp.json()
    symbols = []
    for s in data.get("data", []):
        # quoteCoin — валюта котировки
        if s["quoteCoin"] == "USDT" and s["status"] == "online":
            symbols.append(s["symbol"])
    return symbols


# -------------------------------
#   Получаем все цены крипты (в USDT) (Bitget)
# -------------------------------
def get_all_crypto_prices():
    resp = requests.get(BITGET_TICKERS_URL)
    resp.raise_for_status()
    data = resp.json()
    prices = {}
    for item in data.get("data", []):
        symbol = item["symbol"]
        # lastPr — последняя цена на Bitget
        prices[symbol] = float(item["lastPr"])
    return prices


# -------------------------------
#  Получаем цену крипты в USDT (Bitget)
# -------------------------------
def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    spot_symbols = get_spot_usdt_symbols()

    pair_usdt = f"{symbol}USDT"
    if pair_usdt not in spot_symbols:
        return False

    prices = get_all_crypto_prices()
    price_usdt = prices.get(pair_usdt)
    if price_usdt is None:
        return False

    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }


# -------------------------------
#      ТЕСТ
# # -------------------------------
# if __name__ == "__main__":
#     coin = input("Введите символ криптовалюты (например BTC): ").strip()
#     result = get_crypto_price_in_usdt(coin)
#
#     if isinstance(result, dict):
#         print(f"{result['symbol']}/USDT = {result['price_usdt']} USDT")
#     else:
#         print("Пара не найдена или ошибка API")
