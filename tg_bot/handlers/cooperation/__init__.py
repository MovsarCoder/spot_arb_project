from aiogram import Router

router = Router()

from .cooperation import router as cooperation_handler_router
router.include_router(cooperation_handler_router)