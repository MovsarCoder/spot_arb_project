import requests

MEXC_BASE = "https://api.mexc.com"
EXCHANGE_INFO = f"{MEXC_BASE}/api/v3/exchangeInfo"
TICKER_PRICE = f"{MEXC_BASE}/api/v3/ticker/price"


def get_spot_usdt_symbols():
    resp = requests.get(EXCHANGE_INFO)
    resp.raise_for_status()
    data = resp.json()
    symbols = [
        s["symbol"]
        for s in data.get("symbols", [])
        if s.get("quoteAsset") == "USDT" and s.get("isSpotTradingAllowed")
    ]
    return symbols


def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    pair = f"{symbol}USDT"
    if pair not in get_spot_usdt_symbols():
        return False

    resp = requests.get(TICKER_PRICE, params={"symbol": pair})
    resp.raise_for_status()
    data = resp.json()
    price_usdt = float(data["price"])
    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }

# # ===================== TEST =====================
# if __name__ == "__main__":
#     coin = input("Введите символ криптовалюты (например BTC): ").strip()
#     res = get_crypto_price_in_usdt(coin)
#     if res:
#         print(f"{res['symbol']}/USDT = {res['price_usdt']} USDT")
#     else:
#         print("Пара не найдена или ошибка API")
