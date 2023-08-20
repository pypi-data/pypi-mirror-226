from functools import cached_property

from fastapi_amis_admin import amis
from fastapi_amis_admin.models import Field
from loguru import logger
from pydantic import BaseModel
from wechatpayv3 import WeChatPay, WeChatPayType


class WxPayCfg(BaseModel):
    """微信支付配置"""

    class Config:
        keep_untouched = (cached_property,)

    appid: str = Field("", title="小程序appid")
    appid_h5: str = Field("", title="公众号appid")

    mch_name: str = Field("", title="商户名称")
    mch_id: str = Field(..., title="商户号")
    api_key: str = Field(..., title="商户平台设置的密钥")
    cert_serial_no: str = Field(..., title="证书序列号")
    mch_cert_dir: str = Field(None, title="商户平台证书目录")
    mch_key: str = Field("", title="商户平台证书key",amis_form_item=amis.Textarea())
    # mch_cert: str = Field("", title="商户平台证书cert")
    notify_url: str = Field(
        "",
        title="微信通知回调地址",
        description="该链接是通过基础下单接口中的请求参数“notify_url”来设置的，要求必须为https地址。"
        "请确保回调URL是外部可正常访问的，且不能携带后缀参数，否则可能导致商户无法接收到微信的回调通知信息。"
        "回调URL示例：“https://pay.weixin.qq.com/wxpay/pay.action”",
    )

    @cached_property
    def wxpay_client(self) -> WeChatPay:
        """微信支付客户端.缓存对象属性,防止重复创建"""
        return WeChatPay(
            wechatpay_type=WeChatPayType.JSAPI,
            mchid=self.mch_id,
            private_key=self.mch_key,
            cert_serial_no=self.cert_serial_no,
            apiv3_key=self.api_key,
            appid=self.appid,
            notify_url=self.notify_url,
            cert_dir=self.mch_cert_dir,
            logger=logger,
            partner_mode=False,
            proxy=None,
        )
