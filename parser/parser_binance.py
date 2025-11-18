import requests

BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_EXCHANGE_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"


# -------------------------------
#   Получаем список пар *крипта/USDT*
# -------------------------------
def get_spot_usdt_symbols():
    resp = requests.get(BINANCE_EXCHANGE_INFO_URL)
    resp.raise_for_status()
    data = resp.json()

    symbols = []
    for s in data["symbols"]:
        if s["quoteAsset"] == "USDT" and s["isSpotTradingAllowed"]:
            symbols.append(s["symbol"])
    return symbols


# -------------------------------
#   Получаем все цены крипты (в USDT)
# -------------------------------
def get_all_crypto_prices():
    resp = requests.get(BINANCE_PRICE_URL)
    resp.raise_for_status()
    return {item["symbol"]: float(item["price"]) for item in resp.json()}


# -------------------------------
#  Получаем цену крипты в USDT
# -------------------------------
def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    spot_symbols = get_spot_usdt_symbols()

    pair_usdt = f"{symbol}USDT"
    if pair_usdt not in spot_symbols:
        return False

    prices = get_all_crypto_prices()
    price_usdt = prices[pair_usdt]

    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }


# -------------------------------
#      ТЕСТ
# -------------------------------
# if __name__ == "__main__":
#     coin = input("Введите символ криптовалюты (например BTC): ").strip()
#     result = get_crypto_price_in_usdt(coin)
#
#     if isinstance(result, dict):
#         print(f"{result['symbol']}/USDT = {result['price_usdt']} USDT")
#     else:
#         print(result)
