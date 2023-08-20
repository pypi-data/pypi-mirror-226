from typing import Annotated

from fastapi import APIRouter, Body
from fastapi_amis_admin.crud import BaseApiOut

from faa_wechat.oauth_base.deps import OAuthUserByTokenD
from faa_wechat.oauth_base.models import OAuthUser

router = APIRouter(tags=["微信授权公用"])


@router.post(
    "/get_oauth_user_info",
    response_model=BaseApiOut[OAuthUser],
)
def get_oauth_user_info(
    wx_user: OAuthUserByTokenD,
):
    """获取当前登录用户微信授权信息"""
    return BaseApiOut(data=wx_user)


@router.post(
    "/update_nickname_and_avatar",
    response_model=BaseApiOut,
)
def update_nickname_and_avatar(
    wx_user: OAuthUserByTokenD,
    nickname: Annotated[str, Body(title="昵称", max_length=40)] = None,
    avatar: Annotated[str, Body(title="头像", max_length=255)] = None,
):
    """更新用户昵称或者头像.
    通过头像昵称填写组件获取用户信息,要求微信基础库>=2.21.2。
    - 参考文档: https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/userProfile.html
    """
    if nickname and nickname != wx_user.nickname:
        wx_user.nickname = nickname
        wx_user.user.nickname = nickname
    if avatar and avatar != wx_user.avatar:
        wx_user.avatar = avatar
        wx_user.user.avatar = avatar
    return BaseApiOut(msg="更新成功")
