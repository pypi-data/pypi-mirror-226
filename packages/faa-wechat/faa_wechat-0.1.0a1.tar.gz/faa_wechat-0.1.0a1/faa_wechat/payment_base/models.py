import json
from datetime import datetime, timedelta
from typing import Optional, Tuple

from fastapi_amis_admin import amis
from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.exceptions import ApiError
from fastapi_user_auth.auth.models import (
    BaseUser,
    CreateTimeMixin,
    PkMixin,
    UpdateTimeMixin,
    User,
)
from pydantic import validator
from sqlalchemy.orm import object_session
from sqlmodel import Relationship, SQLModel
from faa_utils.utils.random_ import random_trade_no

from faa_wechat.payment_base.enums import ErrorCode, PayLogType, PayOrderStatus, WxPayType


class EndTimeMixin(SQLModel):
    end_time: Optional[datetime] = Field(default_factory=datetime.now, title="结束时间")


class BasePayUser(BaseUser):
    balance: float = Field(default=0, title="余额")
    vip_end_time: Optional[datetime] = Field(default=None, title="vip结束时间", description="如果为None则表示不是vip,如果不为None则表示vip到期时间.")
    score: int = Field(default=0, title="积分")

    def update_vip_end_time(self, dt: timedelta):
        """更新vip结束时间"""
        now = datetime.now()
        old_end_time = max(self.vip_end_time, now) if self.vip_end_time else now  # 旧VIP到期时间
        self.vip_end_time = old_end_time + dt  # 新VIP到期时间

    # 是否为vip
    @property
    def is_vip(self):
        return self.vip_end_time is not None and self.vip_end_time > datetime.now()

    @property
    def role_display(self):
        return "VIP用户" if self.is_vip else "普通用户"


class PayUser(BasePayUser, User, table=True):
    def update_balance(self, value: float, log: "BalanceLog" = None) -> Tuple[int, str]:
        """
        更新余额. 充值、消费; 并记录日志
        Args:
            value: >0: 充值金额;<0  消费金额;=0: 无效操作
            log: 支付日志

        Returns:   返回结果.
            成功:(1, '当前余额: xxx')
            失败:(code, '错误信息')

        """
        if value == 0:
            return 1, str(self.balance)
        balance = self.balance + value
        if balance < 0:
            raise ApiError(status=ErrorCode.BALANCE_NOT_ENOUGH)
        self.balance = balance
        # 保存日志
        log = log or BalanceLog()
        log.value = value
        log.value1 = self.balance
        log.user_id = self.id
        object_session(self).add(log)
        return 1, f"当前余额: {self.balance}"

    def update_score(self, value: int, log: "ScoreLog" = None) -> Tuple[int, str]:
        """
        更新积分. 充值、消费; 并记录日志
        Args:
            value: >0: 充值积分;<0  消费积分;=0: 无效操作
            log: 支付日志

        Returns:   返回结果.
            成功:(1, '当前积分: xxx')
            失败:(code, '错误信息')

        """
        if value == 0:
            return 1, str(self.score)
        score = self.score + value
        if score < 0:
            raise ApiError(status=ErrorCode.ACCOUNT_SCORE_NOT_ENOUGH)
        self.score = score
        # 保存日志
        log = log or ScoreLog()
        log.value = value
        log.value1 = self.score
        log.user_id = self.id
        object_session(self).add(log)
        return 1, f"当前积分: {self.score}"


class BalanceLog(PkMixin, CreateTimeMixin, UpdateTimeMixin, table=True):
    """账号余额消费日志"""

    __tablename__ = "payment_balance_log"

    value: float = Field(0, title="变化值", description="这里的变化值是平台余额;>0: 充值;<0  消费;")
    type: PayLogType = Field(default=PayLogType.CONSUME, title="类型")
    value1: float = Field(0, title="当前余额")
    desc: str = Field(default="", title="详情")
    user_id: int = Field(None, title="用户ID", foreign_key="auth_user.id")
    # # 状态
    # status: PayLogStatus = Field(
    #     default=None, title="状态", description=str(PayLogStatus.choices)
    # )
    # 附加数据
    attach: str = Field(default="", title="附加数据", description="用来存储一些额外的数据,例如商品id,订单id等")
    user: PayUser = Relationship(
        sa_relationship_kwargs={
            "enable_typechecks": False,
        }
    )

    @validator("attach", pre=True, always=True)
    def validate_attach(cls, v):
        return json.dumps(v) if isinstance(v, dict) else v


class PayOrder(PkMixin, CreateTimeMixin, UpdateTimeMixin, table=True):
    """微信支付订单"""

    __tablename__ = "payment_order"
    trade_type: str = Field(None, title="交易类型")
    trade_no: str = Field(default_factory=random_trade_no, title="商户订单号", max_length=40, index=True)
    total_fee: int = Field(0, title="总金额，单位分", gt=0)
    body: str = Field(default="", title="订单描述")
    status: PayOrderStatus = Field(PayOrderStatus.UNPAID, title="状态")
    pay_type: WxPayType = Field(None, title="支付方式")
    pay_time: Optional[datetime] = Field(default=None, title="支付时间")
    attach: str = Field(
        default=None,
        title="附加数据",
        amis_form_item=amis.Editor(language="json"),
        amis_table_column="json",
    )
    openid: str = Field(default=None, title="openid")

    # user_id: Optional[int] = Field(None, title = '用户', foreign_key = 'auth_user.id')
    #
    # user: PayUser = Relationship(
    #     sa_relationship_kwargs = {
    #         "enable_typechecks": False,
    #     }
    # )

    @validator("attach", pre=True, always=True)
    def validate_attach(cls, v):
        return json.dumps(v) if isinstance(v, dict) else v

    @property
    def attach_dict(self):
        return json.loads(self.attach) if self.attach else {}


class ScoreLog(PkMixin, CreateTimeMixin, UpdateTimeMixin, table=True):
    """账号积分消费日志"""

    __tablename__ = "payment_score_log"

    value: float = Field(0, title="积分变化")
    type: PayLogType = Field(default=PayLogType.CONSUME, title="类型")
    value1: float = Field(0, title="当前余额")
    desc: str = Field(default="", title="详情")
    user_id: int = Field(None, title="用户ID", foreign_key="auth_user.id")
    # # 状态
    # status: PayLogStatus = Field(
    #     default=None, title="状态", description=str(PayLogStatus.choices)
    # )
    # 附加数据
    attach: str = Field(default="", title="附加数据", description="用来存储一些额外的数据,例如商品id,订单id等")
    user: PayUser = Relationship(
        sa_relationship_kwargs={
            "enable_typechecks": False,
        }
    )