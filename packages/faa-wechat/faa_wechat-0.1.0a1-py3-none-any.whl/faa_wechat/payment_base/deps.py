from typing import Annotated

from fastapi import Query

from faa_wechat.payment_base.enums import WxPayType

WxPayTypeQ = Annotated[
    WxPayType,
    Query(title="微信支付类型", description=str(WxPayType.choices)),
]
