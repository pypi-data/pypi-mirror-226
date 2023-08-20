from typing import Annotated

from fastapi_config import globals as g
from fastapi import Depends, Query
from fastapi_user_auth.auth.exceptions import ApiError
from wechatpy import WeChatOAuthException

from faa_wechat.oauth_base.enums import OAuthErrorCode, OAuthType
from faa_wechat.oauth_base.models import BaseOAuthUser

from .config import WxOAuthCfg

H5LoginCodeQ = Annotated[
    str, Query(title="微信授权code", min_length=20, max_length=32, description="用户通过微信h5授权后, 微信会在重定向链接中附加返回一个code, 用于获取用户信息")
]

H5RedirectUriQ = Annotated[str, Query(description="授权后重定向的回调链接地址")]
H5ScopeQ = Annotated[
    str,
    Query(
        description="应用授权作用域，snsapi_base（不弹出授权页面，直接跳转，只能获取用户openid）,"
        "snsapi_userinfo（弹出授权页面，可通过openid拿到昵称、性别、所在地。并且，即使在未关注的情况下，只要用户授权，也能获取其信息）",
    ),
]
H5StateQ = Annotated[str, Query(description="重定向后会带上state参数，开发者可以填写a-zA-Z0-9的参数值，最多128字节")]


async def get_oauth_cfg() -> WxOAuthCfg:
    """获取微信公众号配置"""
    return await g.config_store.get(WxOAuthCfg)


WxOAuthCfgD = Annotated[WxOAuthCfg, Depends(get_oauth_cfg)]


# 通过微信授权code,获取openid,并返回登录用户
def h5_get_wx_user_by_code(
    cfg: WxOAuthCfgD,
    code: H5LoginCodeQ,
) -> BaseOAuthUser:
    """通过微信授权code,获取openid,并返回登录用户"""
    # 微信公众平台api客户端

    try:
        info = cfg.oauth_client.fetch_access_token(code=code)
        wx_user = BaseOAuthUser(
            openid=info["openid"],
            unionid=info.get("unionid", None),
            session_key=info["access_token"],
            type=OAuthType.JSAPI,
            appid=cfg.appid,
        )
    except WeChatOAuthException as e:
        raise ApiError(status=OAuthErrorCode.CODE_ERROR) from e
    user_info = cfg.oauth_client.get_user_info(openid=wx_user.openid, access_token=wx_user.session_key)
    wx_user.nickname = user_info["nickname"]
    wx_user.avatar = user_info["headimgurl"]
    return wx_user


BaseOAuthUserByH5CodeD = Annotated[BaseOAuthUser, Depends(h5_get_wx_user_by_code)]
