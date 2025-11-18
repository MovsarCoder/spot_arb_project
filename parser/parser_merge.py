import asyncio
from .parser_binance import get_crypto_price_in_usdt as binance_result
from .parser_bybit import get_crypto_price_in_usdt as bybit_result
from .parser_bingX import get_crypto_price_in_usdt as bingx_result
from .parser_bitget import get_crypto_price_in_usdt as bitget_result
from .parser_coinEx import get_crypto_price_in_usdt as coinex_result
from .parser_gateio import get_crypto_price_in_usdt_gateio as gateio_result
from .parser_htx import get_crypto_price_in_usdt as htx_result
from .parser_kukoin import get_crypto_price_in_usdt as kuko_result
from .parser_mexc import get_crypto_price_in_usdt as mexc_result
from .parser_okx import get_crypto_price_in_usdt_okx as okx_result
from .parser_phemex import get_crypto_price_in_usdt_phemex as phemex_result


async def parser_merge(coin: str):
    # Запускаем синхронные функции в отдельных потоках
    binance_task = asyncio.to_thread(binance_result, coin)
    bybit_task = asyncio.to_thread(bybit_result, coin)
    bingx_task = asyncio.to_thread(bingx_result, coin)
    bitget_task = asyncio.to_thread(bitget_result, coin)
    coinex_task = asyncio.to_thread(coinex_result, coin)
    gateio_task = asyncio.to_thread(gateio_result, coin)
    htx_task = asyncio.to_thread(htx_result, coin)
    kuko_task = asyncio.to_thread(kuko_result, coin)
    mexc_task = asyncio.to_thread(mexc_result, coin)
    okx_task = asyncio.to_thread(okx_result, coin)
    phemex_task = asyncio.to_thread(phemex_result, coin)

    # Ждём выполнения обоих
    binance, bybit, bingx, bitget, coinex, gateio, htx, kuko, mexc, okx, phemex = await asyncio.gather(binance_task, bybit_task, bingx_task, bitget_task, coinex_task, gateio_task, htx_task, kuko_task,
                                                                                                       mexc_task, okx_task, phemex_task)

    return {
        "Binance": binance if binance else None,
        "Bybit": bybit if bybit else None,
        "Bingx": bingx if bingx else None,
        "Bitget": bitget if bitget else None,
        "CoinEx": coinex if coinex else None,
        "GateIO": gateio if gateio else None,
        "HTX": htx if htx else None,
        "Kuko": kuko if kuko else None,
        "MExC": mexc if mexc else None,
        "OKX": okx if okx else None,
        "Phemex": phemex if phemex else None,
    }
