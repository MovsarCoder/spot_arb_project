import requests

GATEIO_API_BASE = "https://api.gateio.ws/api/v4"
GATEIO_SPOT_TICKERS = f"{GATEIO_API_BASE}/spot/tickers"


def get_all_crypto_prices_gateio():
    """Возвращает словарь { 'BTC': price_usdt, ... }"""
    try:
        resp = requests.get(GATEIO_SPOT_TICKERS, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {}

    prices = {}
    for ticker in data:
        pair = ticker.get("currency_pair", "")
        if not pair.endswith("_USDT"):
            continue
        base = pair.split("_")[0].upper()
        last = ticker.get("last")
        if last is None:
            continue
        prices[base] = float(last)
    return prices


def get_crypto_price_in_usdt_gateio(symbol: str):
    symbol = symbol.upper()
    prices = get_all_crypto_prices_gateio()
    if symbol not in prices:
        return False
    return {"symbol": symbol, "price_usdt": prices[symbol]}


# -------------------------------
#      ТЕСТ
# -------------------------------
if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    res = get_crypto_price_in_usdt_gateio(coin)
    if res:
        print(f"{res['symbol']}/USDT: {res['price_usdt']:.8f}")
    else:
        print(f"🏦 Биржа: Gate.io\n  💵 {coin.upper()}/USDT: — (нет данных)")
