import pytest

from .deps import h5_get_wx_user_by_code


@pytest.mark.skip
def test_get_user_by_code(session):
    """https://xq2.118.ymkt8.cn/oauth/wechat/h5/login?code=061FL40w3HVnoZ2tDo3w3ieBL72FL40J&state="""
    res = h5_get_wx_user_by_code(
        code="001zi4Ga1H8G4E0YvuIa1yCgqW1zi4G9",
    )
    print(res)
