import pytest
from wechatpy.crypto import WeChatWxaCrypto

from faa_wechat.oauth_base.enums import OAuthErrorCode
from faa_wechat.oauth_base.models import OAuthUser
from faa_wechat.oauth_wechat_applet.apis import get_phone_number
from faa_wechat.oauth_wechat_applet.deps import applet_get_base_wx_user_by_code
from faa_wechat.oauth_wechat_applet.schemas import WxEncryptedData


@pytest.mark.skip(reason="需要真实的code")
def test_oauth_user_get_or_create(session):
    ouser = OAuthUser.get_or_create(session, openid="oE6ug4rsR6G_gGFIu6984vF5LZKA")
    assert ouser
    assert ouser.openid == "oE6ug4rsR6G_gGFIu6984vF5LZKA"
    assert ouser.user.username == "oE6ug4rsR6G_gGFIu6984vF5LZKA"
    session.commit()


@pytest.mark.skip(reason="需要真实的code")
def test_get_wx_user_by_code(session):
    # 错误的code
    wx_user = applet_get_base_wx_user_by_code(code="oE6ug4rsR6G_gGFIu6984vF5LZKA")
    assert wx_user is None


def test_api_login(sync_client):
    # 错误的code
    res = sync_client.get("/oauth/wechat/login?code=033ck60w3ZdydZ2I1b2w3l5Yvw4ck60y")
    assert res.status_code == 200
    assert res.json()["status"] == OAuthErrorCode.CODE_ERROR
    # # 正确的code
    # res = mClient.get('/oauth/wx_oauth_login?code=033yMq0w3mpDeZ2P9k3w3pDRzS0yMq0Z')
    # print(res.json())
    # assert res.status_code == 200
    # assert res.json()['status'] == 0
    # assert 'token' in res.json()['data']
    # assert 'openid' in res.json()['data']


# 测试微信获取用户信息
@pytest.mark.skip(reason="需要真实的code")
def test_api_get_userinfo(sync_client):
    res = sync_client.post(
        "/wechat/applet/get_userinfo",
        params={
            "code": "023DoA100dVYhP1aYe100rih2Q2DoA1B",
        },
        json={
            "iv": "P+zRc52j6kbikduTyajAuw==",
            "encryptedData": "LXsECz6hh3gkc1AHsOF1M1ekNFGbeB2uvynydBlr9nJHjghzKxAtorse8e9jFTYG3yWAf3/12BSis"
            "/qCRuttE91MtsS32CEc3r3zNWmVjpsOWRmDctpXjFvJXw42EOQat2d/RoISsUVFphiB"
            "+z2YbJ9l732SWsTLBYircxeqIr0tZLVQtWR86xolTxBpFqU"
            "+YllS4ofammpcsrb7pWe2tdHl9NXS05sqEy7OUc30VgsEQu3jimolkSZ6NbXY0/L+Cvw"
            "+kxepAYwVNuqjwjRDMRSeBHiUDEgC2qm1FtJUnfq7UPQUZy6GBnZx1sRxun7NtDPRuUjn8yq9qavxaW"
            "+lXXFg7zi7xHYDhZrKl3SFtQqZ8swTz2CvG0RCF/exHwZ4E2ozF/aq8njz9klXavwdHx2VfwbgJIJtJ9+Jw0F"
            "/BUskc8Ij1wogvSj/J0YTZ4WCbR+n9DTqtVUeMgUvCNlt9Q==",
            # noqa: E501
        },
    )
    print(res.json())
    # assert res.status_code == 200
    # assert res.json()["status"] == 0
    # assert res.json()["data"]["nickName"] == "微信用户"


# 测试微信获取用户手机号
@pytest.mark.skip("需要真实的code")
def test_api_get_phone_number(sync_client):
    res = sync_client.post(
        "/oauth/wechat/get_phone_number",
        params={
            "code": "073PcHFa1LTVUD0zxuHa1uQxlN1PcHFD",
        },
        json={
            "iv": "57IEfyVZ69eauwoLT8cz/w==",
            "encryptedData": "vOezZaVMEVhZ+IAsYwYU2OsZyt+iLg==",  # noqa: E501
        },
    )
    print(res)
    print(res.text)
    # assert res.status_code == 200
    # assert res.json()['status'] == 0
    # assert res.json()['data']['nickName'] == '微信用户'


@pytest.mark.skip(reason="需要真实的userinfo")
def test_get_phone_number(session):
    res = get_phone_number(
        WxEncryptedData(
            iv="K130nGg556AOzC4CfrdPdw==",
            encryptedData="WTVRH7jL8prszoHYOV5NTtXMvw4Q==",  # noqa: E501
        ),
        wx_user=OAuthUser(
            id=3,
            nickname="",
            session_key="n4a59Agt6F+FIzE+3qbdTQ==",
            user_id=42,
            openid="oMbfs5eeaZCkg6Kvbusaq3Tc6Fzo",
            avatar="",
        ),
        session=session,
    )
    print(res)


def test_decrpt():
    """
    get_userinfo iv='6b3R7Nflx2Kyqz++vSNqVQ=='
    encrypted_data='vDOljJhkIQ79Rc9lfBrUV4MA/loz3VG6zDOYBf6ow4JYWkXCDQt5IimlhFumlEP00oBwdGRAzBnhpvYNVq7
    +wA8PBlJATeqxfz0pACgmAYKkbA9zhfzp94fDs9eSBcum01SK7Y2RKgpZh3PT4p7WgmZHFGs8naijsSByF/Kxp78M+pIVwMnpg0HeXfQ6dUrysvLTkgjlHaKyY
    /gV4JTxm930442UC+LQ9tQLVzS9Xu+zzrhCM/3AS/CPXpO7A2gkISRTZNmAI6uTeSigYGcMxEeDY33Pxc
    +xPUvvNf1N5D1KiR9PyqqelJlPQsA9IX1SuVkSpziRJ8hfdpX2x71JC9Cwa9tz2w1TP/g/9E0SzpehQEcRKvZvWFLasKAQDHq
    +cv9eblMSXx4jSjIHiXuERSBbZw80wR8rgT0rgx6g2K9V1gFntrLtDLA4Vutxo++3' Ytsel8UqO9jrL6Z1a6ua8w== wx988ed18a1f1871f7

    """
    crypt = WeChatWxaCrypto("Ytsel8UqO9jrL6Z1a6ua8w==", "6b3R7Nflx2Kyqz++vSNqVQ==", "wx988ed18a1f1871f7")

    user_info = crypt.decrypt_message(
        r"vDOljJhkIQ79Rc9lfBrUV4MA/loz3VG6zDOYBf6ow4JYWkXCDQt5IimlhFumlEP00oBwdGRAzBnhpvYNVq7+wA8PBlJATeqxfz0pACgmAYKkbA9zhfzp94fDs9eSBcum01SK7Y2RKgpZh3PT4p7WgmZHFGs8naijsSByF/Kxp78M+pIVwMnpg0HeXfQ6dUrysvLTkgjlHaKyY/gV4JTxm930442UC+LQ9tQLVzS9Xu+zzrhCM/3AS/CPXpO7A2gkISRTZNmAI6uTeSigYGcMxEeDY33Pxc+xPUvvNf1N5D1KiR9PyqqelJlPQsA9IX1SuVkSpziRJ8hfdpX2x71JC9Cwa9tz2w1TP/g/9E0SzpehQEcRKvZvWFLasKAQDHq+cv9eblMSXx4jSjIHiXuERSBbZw80wR8rgT0rgx6g2K9V1gFntrLtDLA4Vutxo++3"
    )
    print(user_info)
