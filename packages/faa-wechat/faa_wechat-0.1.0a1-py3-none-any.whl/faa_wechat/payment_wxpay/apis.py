from typing import Annotated

from faa_utils.deps import RequestBodyD
from fastapi import APIRouter, Body
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import SyncSess
from fastapi_user_auth.auth.exceptions import ApiError
from starlette.requests import Request

from faa_wechat.payment_base.deps import WxPayTypeQ
from faa_wechat.payment_base.enums import ErrorCode, OrderType, WxPayType
from faa_wechat.payment_services.models import PayService
from faa_wechat.payment_wxpay.crud import complete_order, create_order, create_order_pack, create_order_pay_response
from faa_wechat.payment_wxpay.deps import WxOpenId, WxPayCfgD
from faa_wechat.payment_wxpay.schemas import WxPayOrderResult

router = APIRouter()


# 创建微信支付订单
@router.post(
    "/pay",
    response_model=BaseApiOut[WxPayOrderResult],
    # include_in_schema=False
)
def pay(
    session: SyncSess,
    openid: WxOpenId,
    pay_type: WxPayTypeQ,
    cfg: WxPayCfgD,
    value: Annotated[int, Body(title="支付金额,单位分", ge=1)],
    order_type: Annotated[OrderType, Body(title="订单类型")] = OrderType.RECHARGE,
):
    """创建微信支付订单. 返回支付参数"""
    if order_type == OrderType.RECHARGE:  # 充值
        body = f"充值【{value / 100}】元"
        total_fee = value  # 总金额,单位分
    elif order_type == OrderType.SERVICE:  # 购买服务
        service = session.get(PayService, value)
        body = f"购买【{service.name}】"
        total_fee = int(service.price * 100)  # 总金额,单位分
    else:
        raise ApiError(status=ErrorCode.ORDER_TYPE_ERROR)
    return create_order_pay_response(
        session,
        pay_type=pay_type,
        cfg=cfg,
        body=body,
        total_fee=total_fee,  # 总金额,单位分
        openid=openid,
        attach={"order_type": order_type, "value": value},
    )


# noinspection PyProtectedMember
@router.post(
    "/notify",
    name="notify",
    # include_in_schema=False,
)
def notify(
    request: Request,
    session: SyncSess,
    cfg: WxPayCfgD,
    body: RequestBodyD,  # 获取原始请求体; 注意微信支付回调签名必须要原始请求体,否则会报签名错误
):
    """接口文档: https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_5_5.shtml"""
    result: dict = cfg.wxpay_client.callback(
        headers={
            "Wechatpay-Serial": request.headers.get("wechatpay-serial"),
            "Wechatpay-Timestamp": request.headers.get("wechatpay-timestamp"),
            "Wechatpay-Nonce": request.headers.get("wechatpay-nonce"),
            "Wechatpay-Signature": request.headers.get("wechatpay-signature"),
            "Wechatpay-Signature-Type": request.headers.get("wechatpay-signature-type"),
        },
        body=body,
    )
    if not result or result.get("event_type") != "TRANSACTION.SUCCESS":
        return {"code": "FAILED", "message": "失败"}
    resp = result.get("resource")
    # trade_type = resp.get('trade_type')
    # trade_state = resp.get('trade_state')
    # trade_state_desc = resp.get('trade_state_desc')
    # bank_type = resp.get('bank_type')
    # attach = resp.get('attach')
    # success_time = resp.get('success_time')
    # payer = resp.get('payer')
    # amount = resp.get('amount').get('total')
    trade_no = resp.get("out_trade_no")
    trade_type = resp.get("trade_type")
    # 完成订单,更新订单状态,并执行相应的业务逻辑
    result = complete_order(session, trade_no=trade_no, trade_type=trade_type)
    session.flush()
    return result
