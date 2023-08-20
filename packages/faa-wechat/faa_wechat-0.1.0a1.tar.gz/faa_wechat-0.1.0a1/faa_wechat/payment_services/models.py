from fastapi_amis_admin import amis
from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.models import CreateTimeMixin, PkMixin, UpdateTimeMixin
from sqlalchemy import Column, Text

from faa_wechat.payment_services.enums import ServiceType


class PayService(PkMixin, CreateTimeMixin, UpdateTimeMixin, table=True):
    """服务列表"""

    __tablename__ = "payment_service"

    name: str = Field(..., title="服务名称", max_length=20)
    price: float = Field(1, title="服务价格(元)", gt=0)
    value: float = Field(1, title="数值", gt=0, description="例如: 当服务类型为VIP服务时,此数值代表时长(天). 当服务类型为余额充值时,此数值代表充值金额(元). ")
    desc: str = Field(default="", title="描述", max_length=400, amis_form_item="textarea")
    content: str = Field(default="", title="内容", sa_column=Column(Text), amis_form_item=amis.InputRichText())
    type: ServiceType = Field(None, title="服务类型")
    is_active: bool = Field(True, title="是否启用")
    sort: int = Field(default=0, title="排序")
    img: str = Field(
        default="",
        title="介绍图片",
        amis_form_item=amis.InputImage(maxLength=1, maxSize=2 * 1024 * 1024),
        amis_table_column=amis.ColumnImage(width=100, height=60, enlargeAble=True),
    )
