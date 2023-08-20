from typing import Annotated

from fastapi_amis_admin.globals.deps import SyncSess
from fastapi import Depends, Query
from fastapi_user_auth.globals.deps import CurrentUser
from sqlmodel import select

from faa_wechat.oauth_base.enums import OAuthType
from faa_wechat.oauth_base.models import OAuthUser

OAuthTypeQ = Annotated[
    OAuthType,
    Query(
        title="授权类型",
        description=str(OAuthType.choices),
    ),
]


def get_wx_user_by_token(
    session: SyncSess,
    user: CurrentUser,
    oauth_type: OAuthTypeQ = OAuthType.JSAPI,
):
    """登录后的token,获取微信授权用户信息"""
    wx_user: OAuthUser = session.scalar(select(OAuthUser).where(OAuthUser.user_id == user.id, OAuthUser.type == oauth_type))
    if wx_user:
        _ = wx_user.user  # load user
    return wx_user


OAuthUserByTokenD = Annotated[OAuthUser, Depends(get_wx_user_by_token)]
