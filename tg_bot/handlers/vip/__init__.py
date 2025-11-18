from aiogram import Router


router = Router()

from .buy_vip import router as buy_vip_router
router.include_router(buy_vip_router)

from .vip_panel import router as vip_panel_router
router.include_router(vip_panel_router)

from .weekeng_spot_handler import router as weekeng_spot_router
router.include_router(weekeng_spot_router)

from .all_prices_spot_handler import router as all_prices_spot_router
router.include_router(all_prices_spot_router)

