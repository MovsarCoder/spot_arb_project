from aiogram import Router

router = Router()

from .start_handler import router as start_handler
router.include_router(start_handler)

from .profile_handler import router as profile_router
router.include_router(profile_router)

from .information_handler import router as information_router
router.include_router(information_router)