from pydantic import BaseModel, Field


class WxPayOrderResult(BaseModel):
    appId: str = Field(None, title="公众账号ID")
    nonceStr: str = Field(None, title="随机字符串")
    package: str = Field(None, title="统一下单接口返回的 prepay_id 参数值，提交格式如：prepay_id=***")
    signType: str = Field(None, title="签名算法")
    timeStamp: str = Field(None, title="时间戳")
    paySign: str = Field(None, title="签名")
