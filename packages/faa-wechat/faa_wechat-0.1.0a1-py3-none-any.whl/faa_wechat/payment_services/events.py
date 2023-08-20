from sqlalchemy import event
from sqlalchemy.orm import object_session
from sqlmodel import Session, select

from faa_wechat.oauth_base.models import OAuthUser
from faa_wechat.payment_base.enums import OrderType, PayLogType, PayOrderStatus
from faa_wechat.payment_base.models import BalanceLog, PayOrder
from faa_wechat.payment_services.crud import complete_service_order
from faa_wechat.payment_services.models import PayService


@event.listens_for(PayOrder.status, "set")
def receive_set(order, value, old, initiator):
    """监听支付订单状态改变"""
    # 订单支付从待支付变成已支付
    if value == PayOrderStatus.PAID and old == PayOrderStatus.UNPAID:
        # 查询订单微信用户
        session: Session = object_session(order)
        wx_user: OAuthUser = session.scalar(select(OAuthUser).where(OAuthUser.openid == order.openid))
        # 进行业务处理
        if order.attach_dict.get("order_type") == OrderType.RECHARGE:
            # 充值
            value = int(order.attach_dict.get("value")) / 100
            wx_user.user.update_balance(
                value=abs(value),
                log=BalanceLog(type=PayLogType.RECHARGE, desc=f"微信充值: {value}"),
            )
            order.status = PayOrderStatus.COMPLETED  # 充值订单直接完成
        elif order.attach_dict.get("order_type") == OrderType.SERVICE:
            # 购买服务
            service_id = order.attach_dict.get("value")
            service = session.get(PayService, service_id)
            if not service:
                raise ValueError("服务不存在")
            # 完成订单
            complete_service_order(session, service, wx_user.user)
            order.status = PayOrderStatus.COMPLETED  # 购买服务订单直接完成
        else:
            raise ValueError("订单类型错误")
