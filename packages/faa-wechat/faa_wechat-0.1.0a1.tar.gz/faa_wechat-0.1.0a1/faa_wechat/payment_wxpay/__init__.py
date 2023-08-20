from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp

from faa_wechat.payment_base.admin import PaymentApp


def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    from . import admin, apis

    # 注册路由
    router.include_router(apis.router, prefix="/payment/wxpay/v3", tags=["微信支付"])
    # 获取支付管理应用实例
    ins = admin_app.get_admin_or_create(PaymentApp)
    # 注册管理页面
    ins.register_admin(admin.WxPayCfgAdmin)
