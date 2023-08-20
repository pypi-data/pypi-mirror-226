import json
import time
from datetime import datetime
from typing import Tuple

from faa_utils.utils.random_ import random_str, random_trade_no
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import SyncSess

from faa_wechat.payment_base.deps import WxPayTypeQ
from faa_wechat.payment_wxpay.deps import WxPayCfgD
from faa_wechat.payment_wxpay.schemas import WxPayOrderResult
from loguru import logger
from fastapi_user_auth.auth.exceptions import ApiError
from sqlmodel import Session, select
from wechatpayv3 import SignType, WeChatPay

from faa_wechat.payment_base.enums import ErrorCode, OrderType, PayOrderStatus, WxPayType
from faa_wechat.payment_base.models import PayOrder


# 创建微信支付订单
def create_order(
    session: Session,
    wxpay: WeChatPay,  # 微信支付实例
    body: str,
    total_fee: int,  # 总金额,单位分
    openid: str,
    attach: dict = None,
    notify_url: str = None,
    appid: str = None,
    pay_type=None,
) -> Tuple[PayOrder, dict]:
    try:
        trade_no = random_trade_no()
        code, result = wxpay.pay(
            description=OrderType.RECHARGE.label,
            out_trade_no=trade_no,
            amount={"total": total_fee},  # 总金额,单位分
            payer={"openid": openid},  # JSAPI支付必须传openid; appid和openid不匹配
            attach=json.dumps(attach),
            notify_url=notify_url,
            appid=appid,
            pay_type=None,
        )
        result = json.loads(result)
        logger.debug(result)
        prepay_id = result.get("prepay_id")
        if code < 200 or code > 300 or not prepay_id:
            raise ApiError(
                status=ErrorCode.CREATE_ORDER_ERROR,
                msg="创建微信支付订单失败",
                code=result.get("code"),
                error=result,
            )
        # 保存订单
        order = PayOrder(
            trade_no=trade_no,
            total_fee=total_fee,
            body=body,
            pay_type=pay_type,
            openid=openid,
            attach=attach,  # type:ignore
        )
        session.add(order)
        session.flush()
        # 将订单号附加的支付结果中
        result.update({"out_trade_no": trade_no})
        return order, result
    except Exception as e:
        logger.error(e)
        raise ApiError(status=ErrorCode.CREATE_ORDER_ERROR, msg=str(e)) from e


def create_order_pack(wxpay: WeChatPay, prepay_id: str, appid: str) -> dict:
    timestamp = str(int(time.time()))
    noncestr = random_str(8)
    package = f"prepay_id={prepay_id}"
    paysign = wxpay.sign(data=[appid, timestamp, noncestr, package], sign_type=SignType.RSA_SHA256)
    return {
        "appId": appid,
        "timeStamp": timestamp,
        "nonceStr": noncestr,
        "package": f"prepay_id={prepay_id}",
        "signType": "RSA",
        "paySign": paysign,
    }


# 查询订单,并完成订单
def query_and_complete_order(session: Session, wxpay: WeChatPay, trade_no: str) -> dict:
    """查询订单,并完成订单"""
    code, result = wxpay.query(out_trade_no=trade_no)
    result = json.loads(result)
    if code < 200 or code > 300:
        return {"code": "FAILED", "message": "查询微信支付订单失败", "error": result}
    if result.get("trade_state") == "SUCCESS":
        # 订单已支付
        return complete_order(session, trade_no, "JSAPI")
    return {"code": "FAILED", "message": "失败,订单未支付"}


# 完成订单
def complete_order(session: Session, trade_no: str, trade_type: str = "JSAPI") -> dict:
    """完成订单,更新订单状态,并执行相应的业务逻辑.
    - 订单状态为待支付时才会执行业务逻辑.
    - 请注意,此方法不会校验订单是否已支付,请在调用此方法前,先校验订单是否已支付.
    - trade_type: JSAPI,APP,NATIVE
    """
    # 修改订单支付状态为支付成功
    order = session.exec(select(PayOrder).where(PayOrder.trade_no == trade_no)).first()
    if not order:
        return {"code": "FAILED", "message": "失败,订单不存在"}
    if order.status != PayOrderStatus.UNPAID:  # 已支付,防止重复回调
        return {"code": "SUCCESS", "message": "成功"}
    order.status = PayOrderStatus.PAID  # 支付成功
    order.pay_time = datetime.now()
    order.trade_type = trade_type
    return {"code": "SUCCESS", "message": "成功"}

def create_order_pay_response(
    session: SyncSess,
    *,
    pay_type: WxPayTypeQ,
    cfg: WxPayCfgD,
    body: str,
    total_fee: int,  # 总金额,单位分
    openid: str,
    attach: dict = None,
) -> BaseApiOut[WxPayOrderResult]:
    """创建微信支付订单. 返回支付参数"""
    appid = cfg.appid if pay_type == WxPayType.MINIPROG else cfg.appid_h5
    if not appid:
        raise ApiError(status=ErrorCode.CREATE_ORDER_ERROR, msg="appid不存在")
    order, result = create_order(
        session,
        wxpay=cfg.wxpay_client,
        body=body,
        total_fee=total_fee,  # 总金额,单位分
        openid=openid,
        attach=attach,
        appid=appid,
        pay_type=pay_type,
    )
    if order and result:
        return BaseApiOut(data=create_order_pack(cfg.wxpay_client, prepay_id=result.get("prepay_id"), appid=appid))
    return BaseApiOut(status=ErrorCode.CREATE_ORDER_ERROR, msg=ErrorCode.CREATE_ORDER_ERROR.label, data=result)