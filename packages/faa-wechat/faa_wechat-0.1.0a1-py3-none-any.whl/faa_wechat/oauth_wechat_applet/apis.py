import hashlib
from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import AsyncSess
from fastapi_user_auth.auth.exceptions import ApiError
from starlette.requests import Request
from starlette.responses import Response
from wechatpy import WeChatException
from wechatpy.crypto import WeChatWxaCrypto

from faa_wechat.oauth_base.deps import OAuthUserByTokenD
from faa_wechat.oauth_base.enums import OAuthErrorCode
from faa_wechat.oauth_wechat_applet.deps import (
    OAuthUserByCodeD,
    PhoneNumberCodeQ,
    WxAppletCfgD,
)
from faa_wechat.oauth_wechat_applet.schemas import WxEncryptedData
from faa_wechat.oauth_wechat_h5.crud import wx_user_login
from faa_wechat.oauth_wechat_h5.schemas import WxLoginResult

router = APIRouter(tags=["微信小程序授权"])


@router.get(
    "/login",
    response_model=BaseApiOut[WxLoginResult],
)
async def applet_login(
    request: Request,
    response: Response,
    wx_user: OAuthUserByCodeD,
    session: AsyncSess,
):
    """
    通过微信`wx.login`获取授权code,并返回登录标识token和openid.
    - 登录成功后,通过在`Header`或者`Cookie`中设置`Authorization`为`Bearer {token}`来进行用户验证.
    """
    data = await wx_user_login(request, response, wx_user, session)
    return BaseApiOut(data=data)


WxLoginResultD = Annotated[BaseApiOut[WxLoginResult], Depends(applet_login)]


@router.post(
    "/update_phone_number",
    response_model=BaseApiOut[dict],
)
def update_phone_number(
    cfg: WxAppletCfgD,
    wx_user: OAuthUserByTokenD,
    code: PhoneNumberCodeQ,
):
    """
    通过手机号快速验证组件获取用户手机号,要求微信基础库>=2.21.2。
    - 参考文档: https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html
    """
    data = cfg.wxa_client.get_phone_number(code)
    print("update_phone_number", data)
    phoneNumber = data.get("phone_info", {}).get("phoneNumber")
    if phoneNumber:
        wx_user.phone_number = phoneNumber
        if hasattr(wx_user.user, "mobile"):
            wx_user.user.mobile = phoneNumber
        return BaseApiOut(data=data, msg="手机号更新成功")
    return BaseApiOut(status=OAuthErrorCode.UPDATE_USER_INFO_ERROR, msg="手机号更新失败", data=data)


@router.post(
    "/update_nickname_and_avatar",
    response_model=BaseApiOut,
    deprecated=True,
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
    return BaseApiOut(data="更新成功")


@router.post(
    "/get_userinfo",
    response_model=BaseApiOut[dict],
    deprecated=True,
)
def get_userinfo(
    cfg: WxAppletCfgD,
    wx_user: OAuthUserByCodeD,
    login_data: WxLoginResultD,
    data: WxEncryptedData,
):
    """通过微信`wx.getUserProfile`获取用户信息加密数据, 上传到后端更新微信用户信息
    - 本接口已经废弃,请直接在前端获取用户信息,并且调用相关接口更新用户信息.
    相关详情请查看文档.
    - https://blog.csdn.net/heimaqianduan/article/details/129790049
    - https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/userProfile.html
    """
    crypt = WeChatWxaCrypto(wx_user.session_key, data.iv, cfg.appid)
    # print("get_userinfo",data, wx_user.session_key, client.appid)
    try:
        user_info = crypt.decrypt_message(data.encrypted_data)
    except WeChatException as e:
        raise ApiError(status=OAuthErrorCode.UPDATE_USER_INFO_ERROR) from e
    if user_info:  # 更新用户信息
        wx_user.nickname = user_info.get("nickName")
        wx_user.avatar = user_info.get("avatarUrl")
        # 用户昵称更新到用户表
        if wx_user.nickname not in ("微信用户", wx_user.user.nickname):
            wx_user.user.nickname = wx_user.nickname
        # 用户头像更新到用户表
        if not wx_user.user.avatar:
            wx_user.user.avatar = wx_user.avatar
    login_data.data.user = wx_user
    return login_data


@router.post(
    "/get_phone_number",
    response_model=BaseApiOut[dict],
    deprecated=True,
)
def get_phone_number(
    cfg: WxAppletCfgD,
    wx_user: OAuthUserByCodeD,
    login_data: WxLoginResultD,
    data: WxEncryptedData,
):
    """通过微信`wx.getPhoneNumber`获取用户手机号加密数据, 上传到后端更新微信用户手机号信息"""
    crypt = WeChatWxaCrypto(wx_user.session_key, data.iv, cfg.appid)
    try:
        user_info = crypt.decrypt_message(data.encrypted_data)
    except WeChatException as e:  # UnicodeDecodeError JSONDecodeError
        raise ApiError(status=OAuthErrorCode.UPDATE_USER_INFO_ERROR) from e
    if user_info:  # 更新用户信息
        phone = user_info.get("phoneNumber")
        if phone:
            wx_user.phone_number = phone
    login_data.data.user = wx_user
    return login_data


@router.get("/message_callback")
def message_callback(signature: str, timestamp: str, nonce: str, echostr: str, cfg: WxAppletCfgD):
    """微信公众号消息回调"""
    if check_signature(signature, timestamp, nonce, cfg.message_token):
        return echostr
    return "error"


def check_signature(signature: str, timestamp: str, nonce: str, token: str) -> bool:
    tmpArr = [token, timestamp, nonce]
    tmpArr.sort()
    tmpStr = "".join(tmpArr)
    tmpStr = hashlib.sha1(tmpStr.encode()).hexdigest()
    return tmpStr == signature


# 88b77c7291fbbe6ceca18644d0fa8f68f9cba86d&amp;echostr=2968876706446180286&amp;timestamp=1688659370&amp;nonce=989443264
