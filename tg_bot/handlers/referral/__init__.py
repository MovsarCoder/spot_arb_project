from aiogram import Router
from .referral_system import router as referral_system_router

router = Router()

router.include_router(referral_system_router)
