from typing import Annotated

from fastapi import Depends, Query
from fastapi_amis_admin import globals as g
from fastapi_config import globals as g2
from fastapi_amis_admin.globals.deps import AsyncSess
from fastapi_user_auth.auth.exceptions import ApiError
from wechatpy import WeChatClientException

from faa_wechat.oauth_base.enums import OAuthErrorCode, OAuthType
from faa_wechat.oauth_base.models import BaseOAuthUser, OAuthUser
from faa_wechat.oauth_wechat_applet.config import WxAppletCfg

AppletLoginCodeQ = Annotated[
    str,
    Query(
        title="微信登录授权code", min_length=20, max_length=32,
        description="通过`wx.login`获取的授权code; 注意: 该code只能使用一次.请在每次请求中传入新的code."
    ),
]

PhoneNumberCodeQ = Annotated[
    str,
    Query(
        title="获取手机号授权code",
        min_length=32,
        max_length=80,
        description="将 button 组件 open-type 的值设置为 getPhoneNumber，当用户点击并同意之后，可以通过 bindgetphonenumber 事件回调获取到动态令牌code.",
    ),
]


async def get_applet_cfg() -> WxAppletCfg:
    """获取微信公众号配置"""
    return await g2.config_store.get(WxAppletCfg)


WxAppletCfgD = Annotated[WxAppletCfg, Depends(get_applet_cfg)]


# 通过微信授权code,获取openid,并返回登录用户
def applet_get_base_wx_user_by_code(
    cfg: WxAppletCfgD,
    code: AppletLoginCodeQ,
) -> BaseOAuthUser:
    """通过微信授权code,获取openid,并返回登录用户"""
    try:
        info = cfg.wxa_client.code_to_session(js_code=code)
        openid = info.get("openid")
        unionid = info.get("unionid")
        session_key = info.get("session_key")
    except WeChatClientException as e:  # 微信code换取openid失败
        raise ApiError(status=OAuthErrorCode.CODE_ERROR) from e
    return BaseOAuthUser(
        appid=cfg.appid,
        openid=openid,
        unionid=unionid,
        session_key=session_key,
        type=OAuthType.APPLET,
    )


BaseOAuthUserD = Annotated[BaseOAuthUser, Depends(applet_get_base_wx_user_by_code)]


async def get_wx_user_by_code(
    session: AsyncSess,
    base_wx_user: BaseOAuthUserD,
):
    """通过微信授权code,获取openid,并返回登录用户"""
    wx_user = await session.run_sync(
        OAuthUser.get_or_create,
        openid=base_wx_user.openid,
        unionid=base_wx_user.unionid,
        type=OAuthType.APPLET,
        session_key=base_wx_user.session_key,
        appid=base_wx_user.appid,
    )
    return wx_user


OAuthUserByCodeD = Annotated[OAuthUser, Depends(get_wx_user_by_code)]
