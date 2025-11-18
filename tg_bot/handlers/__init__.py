from aiogram import Router

router = Router()


from .admin import router as admin_routers
router.include_router(admin_routers)

from .commands import router as command_routers
router.include_router(command_routers)

from .cooperation import router as cooperation_routers
router.include_router(cooperation_routers)

from .referral import router as referral_routers
router.include_router(referral_routers)

from .vip import router as vip_routers
router.include_router(vip_routers)