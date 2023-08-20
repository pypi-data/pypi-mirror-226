import uuid
from datetime import datetime

from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.models import (
    CreateTimeMixin,
    PkMixin,
    UpdateTimeMixin,
    User,
)
from sqlmodel import Relationship

from faa_wechat.payment_base.enums import PayCardStatus


class PayCard(PkMixin, CreateTimeMixin, UpdateTimeMixin, table=True):
    """充值卡"""

    __tablename__ = "payment_card"

    sid: str = Field(default_factory=lambda: str(uuid.uuid4()), title="卡号", max_length=40, index=True)
    value: float = Field(10, title="卡值")
    status: PayCardStatus = Field(PayCardStatus.UNUSED, title="状态")
    user_id: int = Field(None, title="使用用户", foreign_key="auth_user.id")
    creator_id: int = Field(None, title="创建者", foreign_key="auth_user.id")

    user: User = Relationship(sa_relationship_kwargs={"foreign_keys": "PayCard.user_id", "enable_typechecks": False})
    creator: User = Relationship(sa_relationship_kwargs={"foreign_keys": "PayCard.creator_id", "enable_typechecks": False})

    def use_card(self, user_id: int) -> bool:
        """
        将充值卡切换为已使用状态
        Args:
            user_id: 使用者id
        """
        if self.status == PayCardStatus.UNUSED:
            self.status = PayCardStatus.USED
            self.update_time = datetime.now()
            self.user_id = user_id
            return True
        return False
