from sqlalchemy.orm import joinedload
from sqlmodel import select

from .models import OAuthUser


def test_oauth_user(session):
    ouser = session.get(OAuthUser, 3)
    assert ouser.id == 3
    assert ouser.user

async def test_async_get(async_sess):
    await async_sess.run_sync(test_get)

def test_get(session):
    stmt = select(OAuthUser).where(
        # OAuthUser.appid == "123213",
        OAuthUser.openid == "oLqE55KCOeTC3W7D3Pe2j3nIcuKM",
    ).options(joinedload(OAuthUser.user))
    print(stmt)
    wx_user = session.scalar(stmt)
    print(wx_user)
