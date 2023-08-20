from typing import Annotated

from fastapi_config import globals as g
from fastapi import Depends, Query
from starlette.requests import Request

from faa_wechat.payment_wxpay.config import WxPayCfg

WxOpenId = Annotated[str, Query(title="微信用户唯一标识", description="微信用户唯一标识,通过微信授权获取")]


async def get_wxpay_cfg() -> WxPayCfg:
    """获取微信支付配置"""
    return await g.config_store.get(WxPayCfg)


WxPayCfgD = Annotated[WxPayCfg, Depends(get_wxpay_cfg)]


# 获取fastapi请求体,微信支付回调签名必须要原始请求体
async def get_request_body(request: Request):
    return await request.body()
