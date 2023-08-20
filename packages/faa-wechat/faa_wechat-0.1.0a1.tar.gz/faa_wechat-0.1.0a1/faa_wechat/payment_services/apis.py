from typing import List

from fastapi import APIRouter
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import SyncSess
from fastapi_user_auth.globals.deps import CurrentUser
from sqlmodel.sql.expression import select

from faa_wechat.oauth_base.models import OAuthUser
from faa_wechat.payment_base.deps import WxPayTypeQ
from faa_wechat.payment_base.enums import ErrorCode, OrderType, PayLogType
from faa_wechat.payment_base.models import BalanceLog, PayUser
from faa_wechat.payment_services.crud import complete_service_order
from faa_wechat.payment_services.deps import PayServiceD, PayServiceSelect, ServiceTypeQ
from faa_wechat.payment_services.enums import ServiceType
from faa_wechat.payment_services.models import PayService
from faa_wechat.payment_wxpay.apis import pay
from faa_wechat.payment_wxpay.deps import WxOpenId, WxPayCfgD
from faa_wechat.payment_wxpay.schemas import WxPayOrderResult

router = APIRouter()


# 获取服务列表
@router.get(
    "/get_service_list",
    response_model=BaseApiOut[List[PayService]],
    tags=["VIP开通", "用户充值"],
)
def get_service_list(
    session: SyncSess,
    sel: PayServiceSelect,
    type: ServiceTypeQ = ServiceType.VIP,
):
    """获取服务列表"""
    sel = sel.where(PayService.type == type).where(PayService.is_active == True).order_by(PayService.sort)  # noqa:E712
    services = session.exec(sel).all()
    return BaseApiOut(data=[PayService.from_orm(service) for service in services])


# 通过微信支付购买服务
@router.post(
    "/buy_service_by_wxpay",
    response_model=BaseApiOut[WxPayOrderResult],
    tags=["用户充值", "VIP开通"],
)
def buy_service_by_wxpay(
    session: SyncSess,
    user: CurrentUser,
    service: PayServiceD,
    pay_type: WxPayTypeQ,
    openid: WxOpenId,
    cfg: WxPayCfgD,
):
    """通过微信支付购买服务
    - 充值余额,通过微信支付,创建微信支付订单.
    - 开通VIP,通过微信支付,创建微信支付订单.
    """
    if service.type not in [ServiceType.RECHARGE, ServiceType.VIP]:
        return BaseApiOut(status=ErrorCode.SERVICE_TYPE_ERROR, msg="服务类型错误")
    # 微信支付
    wx_user = session.exec(
        select(OAuthUser).where(OAuthUser.user_id == user.id)  # OAuthUser.type == pay_type 只有支付类型和用户openid类型一致的才能支付
    ).first()
    if not wx_user:
        return BaseApiOut(status=ErrorCode.ACCOUNT_NOT_BIND_WX, msg="用户未绑定微信或支付类型错误")
    return pay(session=session, openid=openid, value=service.id, order_type=OrderType.SERVICE, pay_type=pay_type, cfg=cfg)


# 通过余额购买服务
@router.post(
    "/buy_service_by_balance",
    response_model=BaseApiOut[PayUser],
    tags=["VIP开通"],
)
def buy_service_by_balance(
    session: SyncSess,
    user: CurrentUser,
    service: PayServiceD,
):
    """通过余额购买服务
    - 开通VIP,通过余额支付,扣除用户余额.
    """
    if service.type != ServiceType.VIP:
        return BaseApiOut(status=ErrorCode.SERVICE_TYPE_ERROR, msg="服务类型错误")
    # 余额支付
    code, msg = user.update_balance(
        value=-abs(service.price),
        log=BalanceLog(
            type=PayLogType.CONSUME,
            desc=f"购买服务: {service.name}",
            attach=str({"service_id": service.id}),
        ),
    )
    # 完成订单
    complete_service_order(session, service, user)
    session.flush()
    return BaseApiOut(msg="开通成功", data=PayUser.from_orm(user))
