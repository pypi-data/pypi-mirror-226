from fastapi_amis_admin.amis import ColumnImage, InputImage
from fastapi_amis_admin.models import Field
from fastapi_user_auth.auth.models import CreateTimeMixin, PkMixin
from fastapi_user_auth.mixins.models import CUDTimeMixin
from sqlalchemy import ForeignKey
from sqlmodel import Relationship, Session, select
from sqlmodelx import SQLModel

from fastapi_user_auth.globals import UserModel
from .enums import OAuthType


class BaseOAuthUser(SQLModel):
    # appid
    appid: str = Field(default="", title="AppId")
    # 授权openid
    openid: str = Field(default="", title="授权openid")
    # UnionID
    unionid: str = Field(
        None, title="UnionID", description="用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台帐号下会返回，详见 UnionID 机制说明。"
    )
    # 授权昵称
    nickname: str = Field(default="", title="授权昵称")
    # 授权头像
    avatar: str = Field(
        default="",
        title="授权头像",
        amis_form_item=InputImage(maxLength=1, maxSize=2 * 1024 * 1024),
        amis_table_column=ColumnImage(width=50, height=50, enlargeAble=True),
    )
    # 授权类型
    type: OAuthType = Field(default=None, title="授权类型")
    # session_key
    session_key: str = Field(default="", title="会话密钥", description="有效期由微信后台决定,通过要求用户重新登录刷新")
    # 手机号码
    phone_number: str = Field(default="", title="手机号码")


class OAuthUser(PkMixin, CUDTimeMixin, BaseOAuthUser, table=True):
    """微信授权用户"""

    __tablename__ = "oauth_user"
    # 会员ID
    user_id: int = Field(None, title="会员ID", sa_column_args=(ForeignKey("auth_user.id", ondelete="CASCADE"),))

    user: UserModel = Relationship(sa_relationship_kwargs={"foreign_keys": "OAuthUser.user_id", "enable_typechecks": False})

    @classmethod
    def get_or_create(cls, session: Session, openid: str, appid: str, **kwargs) -> "OAuthUser":
        """通过微信openid,创建新用户"""
        # 1.通过openid查询用户
        stmt = select(OAuthUser).where(
            OAuthUser.appid == appid,
            OAuthUser.openid == openid,
        )  # .options(joinedload(OAuthUser.user))  # joinedload(OAuthUser.user) # subqueryload
        wx_user = session.scalar(stmt)
        if wx_user:
            user = wx_user.user  # load user
        else:  # 1.创建微信授权用户
            # 通过openid查询用户
            user = session.scalar(select(UserModel).where(UserModel.username == openid))
            if not user:  # 2.创建新用户
                user = UserModel(
                    username=openid,
                    nickname="微信用户",
                    password=appid,  # type: ignore
                )
            wx_user = OAuthUser(
                openid=openid,
                appid=appid,
                user=user,
                **kwargs,
            )
            session.add(wx_user)
            session.flush()
        return wx_user


class OAuthHistory(PkMixin, CreateTimeMixin, table=True):
    """登录记录"""

    __tablename__ = "oauth_history"

    user_id: int = Field(None, title="会员ID", sa_column_args=(ForeignKey("auth_user.id", ondelete="CASCADE"),))
    ip: str = Field("", title="登录IP", max_length=20)
    client: str = Field("", title="客户端", max_length=20)

    user: UserModel = Relationship(sa_relationship_kwargs={"enable_typechecks": False})
