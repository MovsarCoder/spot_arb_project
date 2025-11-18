import requests

OKX_TICKERS = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

def get_crypto_price_in_usdt_okx(symbol: str):
    symbol = symbol.upper()
    pair = f"{symbol}-USDT"

    resp = requests.get(OKX_TICKERS)
    resp.raise_for_status()
    data = resp.json()

    for item in data.get("data", []):
        if item["instId"] == pair:
            return {"symbol": symbol, "price_usdt": float(item["last"])}
    return False

# ===================== TEST =====================
if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    res = get_crypto_price_in_usdt_okx(coin)
    if res:
        print(f"{res['symbol']}/USDT = {res['price_usdt']} USDT")
    else:
        print("Пара не найдена или ошибка API")
