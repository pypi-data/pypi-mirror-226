import json

import pytest
from faa_utils.utils.random_ import random_trade_no
from wechatpayv3 import WeChatPay

from .crud import complete_order
from .deps import get_wxpay_cfg


@pytest.fixture
async def wxpay_client():
    cfg = await get_wxpay_cfg()
    return cfg.wxpay_client


@pytest.mark.skip
def test_create_order(wxpay_client: WeChatPay):
    openid = "oMbfs5eeaZCkg6Kvbusaq3Tc6Fzo"
    trade_no = random_trade_no()
    code, message = wxpay_client.pay(description="测试订单", out_trade_no=trade_no, amount={"total": 1}, payer={"openid": openid})
    assert code == 200
    assert "prepay_id" in message


@pytest.mark.skip
def test_wx_pay_notify(sync_client):
    data = {
        "id": "EV-2018022511223320873",
        "create_time": "2015-05-20T13:29:35+08:00",
        "resource_type": "encrypt-resource",
        "event_type": "TRANSACTION.SUCCESS",
        "summary": "支付成功",
        "resource": {
            "original_type": "transaction",
            "algorithm": "AEAD_AES_256_GCM",
            "ciphertext": "",
            "associated_data": "",
            "nonce": "",
        },
    }
    res = sync_client.post("/payment/wxpay/v3/notify", json=data)
    # assert res.status_code == 200
    print(res)


@pytest.mark.skip
def test_wx_pay_query(wxpay_client: WeChatPay):
    trade_no = "20221002160534131279"
    code, message = wxpay_client.query(out_trade_no=trade_no)
    message = json.loads(message)
    assert code == 200
    assert "trade_state" in message
    assert message["trade_state"] == "NOTPAY"
    assert message["amount"]["total"] == 18800


@pytest.mark.skip
def test_complete_order(session):
    trade_no = "20221002084051511520"
    result = complete_order(session, trade_no=trade_no)
    print(result)
