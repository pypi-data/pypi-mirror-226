# 第三方授权基础包, 用于拓展实现第三方授权登录
from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    from . import admin, apis

    # 注册路由
    router.include_router(apis.router, prefix="/wechat/base")

    # 注册管理页面
    admin_app.register_admin(admin.OauthApp)
