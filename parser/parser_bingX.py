import requests

BINGX_BASE_URL = "https://open-api.bingx.com"


# -------------------- Получаем все спотовые пары к USDT -------------------- #
def get_bingx_spot_usdt_prices():
    """Возвращает список всех спотовых пар BingX, торгующихся к USDT"""
    url = f"{BINGX_BASE_URL}/openApi/spot/v1/ticker/price"
    resp = requests.get(url)
    resp.raise_for_status()

    items = resp.json().get("data", [])
    result = []

    for item in items:
        symbol = item.get("symbol")
        trades = item.get("trades")
        if not symbol or not trades:
            continue
        price_str = trades[0].get("price")
        if not price_str:
            continue

        parts = symbol.split("_")
        if len(parts) != 2:
            continue
        base, quote = parts
        if quote != "USDT":
            continue

        try:
            price_usdt = float(price_str)
        except ValueError:
            continue

        result.append({
            "symbol": base,
            "price_usdt": price_usdt
        })

    return result


# -------------------- Получаем цену конкретной крипты в USDT -------------------- #
def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    prices_usdt = get_bingx_spot_usdt_prices()

    for p in prices_usdt:
        if p["symbol"] == symbol:
            return {
                "symbol": symbol,
                "price_usdt": p["price_usdt"]
            }

    return False

# -------------------- Пример использования -------------------- #
# if __name__ == "__main__":
#     coin = input("Введите символ криптовалюты (например BTC): ").strip()
#     result = get_crypto_price_in_usdt(coin)
#
#     if isinstance(result, dict):
#         print(f"{result['symbol']}/USDT = {result['price_usdt']:.6f} USDT")
#     else:
#         print(result)
