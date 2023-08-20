from functools import cached_property
from wechatpy import WeChatClient

from pydantic import BaseModel, Field
from wechatpy.client.api import WeChatWxa


class WxAppletCfg(BaseModel):
    """微信小程序配置"""

    class Config:
        keep_untouched = (cached_property,)

    name: str = Field("", title="小程序名称")
    appid: str = Field(..., title="小程序appid")
    secret: str = Field(..., title="小程序secret")
    message_token: str = Field("", title="消息校验token")

    @cached_property
    def client(self) -> WeChatClient:
        """获取微信Api客户端;缓存对象属性防止重复创建"""
        return WeChatClient(self.appid, self.secret)

    @cached_property
    def wxa_client(self) -> WeChatWxa:
        """获取微信小程序api客户端"""
        return self.client.wxa
