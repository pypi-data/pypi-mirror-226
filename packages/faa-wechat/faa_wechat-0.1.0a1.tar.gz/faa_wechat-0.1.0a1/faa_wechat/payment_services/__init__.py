from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    from . import admin, apis, events

    # 注册路由
    router.include_router(apis.router, prefix="/payment/services")
    # 注册管理页面
    admin_app.register_admin(admin.PayServiceAdmin)
