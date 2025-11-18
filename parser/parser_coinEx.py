import requests

COINEX_TICKER_URL = "https://api.coinex.com/v2/spot/ticker"


def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    pair = f"{symbol}USDT"
    resp = requests.get(COINEX_TICKER_URL, params={"market": pair})
    resp.raise_for_status()
    data = resp.json()
    if data["code"] != 0:
        return False
    result = data.get("data", [])
    if not result or len(result) < 1:
        return False
    ticker = result[0]
    price_usdt = float(ticker["last"])
    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }

# if __name__ == "__main__":
#     coin = input("Введите символ криптовалюты (например BTC): ").strip()
#     res = get_crypto_price_in_usdt(coin)
#     if res:
#         print(f"{res['symbol']}/USDT = {res['price_usdt']} USDT")
#     else:
#         print("Пара не найдена или ошибка API")
