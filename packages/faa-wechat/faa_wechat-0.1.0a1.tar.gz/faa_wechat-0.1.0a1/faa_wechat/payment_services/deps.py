from typing import Annotated

from faa_utils.deps import PageSelector
from fastapi import Depends, Query
from fastapi_amis_admin.globals.deps import SyncSess
from fastapi_user_auth.auth.exceptions import ApiError
from sqlmodel.sql.expression import SelectOfScalar

from faa_wechat.payment_base.enums import ErrorCode
from faa_wechat.payment_services.enums import ServiceType
from faa_wechat.payment_services.models import PayService

PayServiceSelect = Annotated[SelectOfScalar[PayService], Depends(PageSelector(PayService))]

ServiceTypeQ = Annotated[
    ServiceType,
    Query(title="服务类型", description=str(ServiceType.choices)),
]


def get_service_by_id(
    session: SyncSess,
    service_id: Annotated[int, Query(title="服务ID", description="根据服务列表获取")],
):
    """根据服务ID获取服务"""
    service = session.get(PayService, service_id)
    if not service:
        raise ApiError(status=ErrorCode.SERVICE_NOT_FOUND)
    return service


PayServiceD = Annotated[PayService, Depends(get_service_by_id)]
