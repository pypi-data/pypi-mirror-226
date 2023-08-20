
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from faa_wechat.oauth_base.models import OAuthHistory, OAuthUser
from faa_wechat.oauth_wechat_h5.schemas import WxLoginResult
from fastapi_user_auth.globals import auth

async def wx_user_login(
    request: Request,
    response: Response,
    wx_user: OAuthUser,
    session: AsyncSession,
) -> WxLoginResult:
    """微信用户登录, 返回token, 并且设置cookie.保存登录记录"""
    token = await auth.backend.token_store.write_token(
        {
            "id": wx_user.user.id,
            "username": wx_user.user.username,
        }
    )
    # 获取顶级域名
    host = request.headers.get("host")
    domain = ".".join(host.split(".")[-2:])
    response.set_cookie("Authorization", f"bearer {token}", domain=domain)
    # 保存登录记录
    history = OAuthHistory(user_id=wx_user.user.id, client="wechat", ip=request.client.host)
    session.add(history)
    return WxLoginResult(token=token, openid=wx_user.openid)
