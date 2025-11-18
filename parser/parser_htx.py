import requests

HTX_API_BASE = "https://api.huobi.pro"  # HTX public API

# -------------------------------
# Получаем список пар *крипта/USDT*
# -------------------------------
def get_spot_usdt_symbols():
    url = f"{HTX_API_BASE}/v1/common/symbols"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    if data["status"] != "ok":
        raise Exception(f"Ошибка API HTX: {data}")

    symbols = []
    for s in data["data"]:
        if s["quote-currency"].upper() == "USDT" and s["state"] == "online":
            symbols.append(s["symbol"].upper())
    return symbols


# -------------------------------
# Получаем цену конкретного символа (в USDT)
# -------------------------------
def get_crypto_price_in_usdt(symbol: str):
    symbol = symbol.upper()
    pair_usdt = f"{symbol}usdt".lower()

    spot_symbols = [s.lower() for s in get_spot_usdt_symbols()]
    if pair_usdt not in spot_symbols:
        return False

    # Берём цену через endpoint тикеров
    url = f"{HTX_API_BASE}/market/detail/merged?symbol={pair_usdt}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "ok" or "tick" not in data:
        raise Exception(f"Ошибка получения цены HTX: {data}")

    price_usdt = float(data["tick"]["close"])  # последнее значение цены
    return {
        "symbol": symbol,
        "price_usdt": price_usdt
    }


# -------------------------------
# ТЕСТ
# -------------------------------
if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    result = get_crypto_price_in_usdt(coin)

    if isinstance(result, dict):
        print(f"{result['symbol']}/USDT = {result['price_usdt']} USDT")
    else:
        print("Пара не найдена или недоступна")
