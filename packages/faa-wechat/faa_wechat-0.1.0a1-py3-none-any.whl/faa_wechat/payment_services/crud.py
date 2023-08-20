from datetime import timedelta

from faa_utils.utils.signals import bind_signal
from fastapi_user_auth.auth.exceptions import ApiError
from sqlmodel import Session


from faa_wechat.payment_base.enums import ErrorCode, PayLogType
from faa_wechat.payment_base.models import BalanceLog, PayUser
from faa_wechat.payment_services.enums import ServiceType
from faa_wechat.payment_services.models import PayService


# 完成服务订单
@bind_signal()
def complete_service_order(session: Session, service: PayService, user: PayUser):
    # 服务处理
    if service.type == ServiceType.RECHARGE:
        # 充值服务
        user.update_balance(
            value=abs(service.value),
            log=BalanceLog(type=PayLogType.RECHARGE, desc=f"购买充值服务: {service.name}"),
        )
    elif service.type == ServiceType.VIP:
        # VIP服务
        user.update_vip_end_time(timedelta(days=service.value))
    else:
        raise ApiError(status=ErrorCode.SERVICE_NOT_FOUND)
