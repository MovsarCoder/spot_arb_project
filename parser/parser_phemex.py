import requests

PHEMEX_API_SPOT = "https://api.phemex.com/md/spot/ticker/24hr"


def get_all_crypto_prices_phemex():
    """
    Возвращает словарь: { 'BTC': price_usdt, ... }
    Если данных нет — возвращает пустой словарь
    """
    try:
        resp = requests.get(PHEMEX_API_SPOT, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return {}  # API не работает

    prices = {}
    for item in data.get("result", []):
        symbol = item.get("symbol", "")
        # Phemex спот-символы — почти всегда контракты типа cBTCUSD
        if not symbol.startswith("c") or not symbol.endswith("USD"):
            continue
        base = symbol[1:-3].upper()
        last_ep = item.get("lastEp")
        if last_ep is None:
            continue
        # lastEp — в "эпсилон" формате, делим на 1e8
        prices[base] = float(last_ep) / 1e8
    return prices


def get_crypto_price_in_usdt_phemex(symbol: str):
    symbol = symbol.upper()
    prices = get_all_crypto_prices_phemex()
    if symbol not in prices:
        return False  # данных нет
    return {"symbol": symbol, "price_usdt": prices[symbol]}


# -------------------------------
#      ТЕСТ
# -------------------------------
if __name__ == "__main__":
    coin = input("Введите символ криптовалюты (например BTC): ").strip()
    result = get_crypto_price_in_usdt_phemex(coin)
    if result:
        print(f"🏦 Биржа: Phemex\n  💵 {result['symbol']}/USDT: {result['price_usdt']:.8f}")
    else:
        print(f"🏦 Биржа: Phemex\n  💵 {coin.upper()}/USDT: — (нет данных)")
