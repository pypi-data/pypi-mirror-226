import time
import uuid
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.globals.deps import AsyncSess
from starlette.datastructures import URL
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from wechatpy import WeChatException

from faa_wechat.oauth_base.enums import OAuthType
from faa_wechat.oauth_base.models import OAuthUser
from faa_wechat.oauth_wechat_h5.crud import wx_user_login
from faa_wechat.oauth_wechat_h5.deps import (
    BaseOAuthUserByH5CodeD,
    H5LoginCodeQ,
    H5RedirectUriQ,
    H5ScopeQ,
    H5StateQ,
    WxOAuthCfgD,
)
from faa_wechat.oauth_wechat_h5.schemas import WxJsApiSign, WxLoginResult

router = APIRouter(tags=["微信公众号H5授权"])


# 获取微信oauth2授权链接
@router.get(
    "/get_authorize_url",
)
def get_authorize_url(
    cfg: WxOAuthCfgD,
    redirect_uri: H5RedirectUriQ = "/",
    scope: H5ScopeQ = "snsapi_userinfo",
    state: H5StateQ = "",
):
    """前端需要将此链接重定向到微信授权页面, 并获取code参数, 用于获取用户openid"""
    client = cfg.oauth_client
    redirect_url = URL(client.redirect_uri).include_query_params(redirect_uri=redirect_uri or "/")
    url = URL(url=f"{client.OAUTH_BASE_URL}oauth2/authorize").include_query_params(
        appid=client.app_id,
        redirect_uri=str(redirect_url),
        scope=scope or client.scope,
        state=state or client.state,
        response_type="code",
    )
    return str(url)


# 微信授权登录重定向地址
@router.get(
    "/redirect",
    # include_in_schema=False,
)
async def redirect(
    request: Request,
    response: Response,
    code: H5LoginCodeQ,
    redirect_uri: H5RedirectUriQ,
    state: H5StateQ = "",
):
    """微信授权登录重定向地址"""
    # todo 重定向地址需要校验白名单
    # sep = "?" if "?" not in redirect_uri else "&"
    # url = f"{redirect_uri}{sep}code={code}&state={state}"
    url = URL(url=redirect_uri).include_query_params(code=code, state=state)
    return RedirectResponse(url=url)


# 获取用户信息
@router.get(
    "/login",
    response_model=BaseApiOut[WxLoginResult],
)
async def h5_login(
    request: Request,
    response: Response,
    session: AsyncSess,
    base_wx_user: BaseOAuthUserByH5CodeD,
):
    """通过微信授权code,获取openid,并返回登录用户
    - 登录成功后,通过在`Header`或者`Cookie`中设置`Authorization`为`Bearer {token}`来进行用户验证.
    """
    # 登录或注册用户
    wx_user = await session.run_sync(
        OAuthUser.get_or_create,
        openid=base_wx_user.openid,
        type=OAuthType.JSAPI,
        session_key=base_wx_user.session_key,
        nickname=base_wx_user.nickname,
        avatar=base_wx_user.avatar,
        appid=base_wx_user.appid,
    )
    # 更新用户信息
    wx_user.user.nickname = base_wx_user.nickname
    wx_user.user.avatar = base_wx_user.avatar
    data = await wx_user_login(request, response, wx_user, session)
    return BaseApiOut(data=data)


"""微信jsapi相关接口"""


# 获取微信jsapi签名
@router.get(
    "/get_jsapi_signature",
    response_model=BaseApiOut[WxJsApiSign],
)
def get_jsapi_signature(
    cfg: WxOAuthCfgD,
    url: Annotated[
        str,
        Query(
            description="需要特别注意url必须是动态获取的,不能写死.url（当前网页的URL，不包含#及其后面部分）。对所有待签名参数按照字段名的ASCII码"
            "从小到大排序（字典序）后，使用URL键值对的格式（即key1=value1&key2=value2…）拼接成字符串string1。",
        ),
    ],
):
    """获取微信jsapi签名.
    - 详细文档: https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/JS-SDK.html#62
    """
    jsapi = cfg.jsapi_client
    try:
        ticket = jsapi.get_jsapi_ticket()
    except WeChatException as e:
        # 常见问题,ip白名单未配置
        return BaseApiOut(status=10000, msg=str(e))
    data = WxJsApiSign(
        appId=jsapi.appid,
        timestamp=int(time.time()),
        nonceStr=uuid.uuid4().hex,
    )
    data.signature = jsapi.get_jsapi_signature(
        noncestr=data.nonceStr,
        ticket=ticket,
        timestamp=data.timestamp,
        url=url,
    )
    return BaseApiOut(data=data)
