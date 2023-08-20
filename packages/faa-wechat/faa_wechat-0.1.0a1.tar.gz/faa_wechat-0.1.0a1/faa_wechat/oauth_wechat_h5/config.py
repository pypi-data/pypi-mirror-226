from functools import cached_property

from pydantic import BaseModel, Field
from wechatpy import WeChatClient, WeChatOAuth
from wechatpy.client.api import WeChatJSAPI


class WxOAuthCfg(BaseModel):
    """微信公众号配置"""

    class Config:
        keep_untouched = (cached_property,)

    name: str = Field("", title="公众号名称")
    appid: str = Field(..., title="公众号appid")
    secret: str = Field(..., title="公众号secret")
    redirect_uri: str = Field(..., title="重定向地址")

    @cached_property
    def oauth_client(self) -> WeChatOAuth:
        """获取微信公众号授权客户端;缓存对象属性防止重复创建"""
        return WeChatOAuth(app_id=self.appid, secret=self.secret, redirect_uri=self.redirect_uri, scope="snsapi_userinfo")

    @cached_property
    def client(self) -> WeChatClient:
        """获取微信Api客户端;缓存对象属性防止重复创建"""
        return WeChatClient(self.appid, self.secret)

    @cached_property
    def jsapi_client(self) -> WeChatJSAPI:
        """获取微信公众号jsapi客户端"""
        return self.client.jsapi
