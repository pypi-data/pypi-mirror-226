# 微信小程序授权登录
# 需要配合基础授权登录插件+微信公众号登录插件使用
from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp

from faa_wechat.oauth_base.admin import OauthApp


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    from . import admin, apis

    # 注册路由
    router.include_router(apis.router, prefix="/wechat/applet")
    # 获取授权管理应用实例
    ins = admin_app.get_admin_or_create(OauthApp)
    # 注册管理页面
    ins.register_admin(admin.WxAppletCfgAdmin)
