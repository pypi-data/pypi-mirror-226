from pydantic import BaseModel

from faa_wechat.oauth_base.models import OAuthUser


class WxLoginResult(BaseModel):
    openid: str = ...
    token_type: str = "bearer"
    token: str = ...
    unionid: str = None


class WxLoginUser(WxLoginResult):
    user: OAuthUser


# 微信Oauth返回的用户信息
class WxOauthResult(BaseModel):
    openid: str = ...
    access_token: str = ...
    scope: str = None
    expires_in: int = None
    refresh_token: str = None


# 微信JsApi签名
class WxJsApiSign(BaseModel):
    appId: str = ...
    timestamp: int = ...
    nonceStr: str = ...
    signature: str = ""
