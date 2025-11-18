from aiogram import Router

router = Router()

from .admin_panel import router as admin_panel_router
router.include_router(admin_panel_router)

from .newsletter import router as newsletter_router
router.include_router(newsletter_router)

from .requests_cooperation import router as requests_cooperation_router
router.include_router(requests_cooperation_router)

from .get_user_id_by_username import router as get_user_id_by_username_router
router.include_router(get_user_id_by_username_router)

from .remove_admin import router as remove_admin_router
router.include_router(remove_admin_router)

from .add_admin import router as add_admin_router
router.include_router(add_admin_router)

from .add_group import router as add_group_router
router.include_router(add_group_router)

from .remove_group import router as remove_group_router
router.include_router(remove_group_router)

from .list_group import router as list_group_router
router.include_router(list_group_router)