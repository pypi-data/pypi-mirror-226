from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.admin import AdminApp
from fastapi_user_auth.auth.models import User
from fastapi_user_auth.mixins.admin import ReadOnlyModelAdmin, SoftDeleteModelAdmin
from sqlmodel.sql.expression import Select
from starlette.requests import Request

from .models import OAuthHistory, OAuthUser


class OauthApp(admin.AdminApp):
    page_schema = amis.PageSchema(label="微信授权", icon="fa fa-weixin")
    router_prefix = "/oauth"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            OAuthUserAdmin,
            OAuthUserLoginHistoryAdmin,
        )


class OAuthUserAdmin(SoftDeleteModelAdmin,admin.ModelAdmin):
    page_schema = amis.PageSchema(label="授权账号", icon="fa fa-user-circle")
    model = OAuthUser
    search_fields = [User.username, OAuthUser.nickname]
    list_display = [
        OAuthUser.user_id,
        User.username,
        User.nickname,
        OAuthUser.type,
        OAuthUser.nickname,
        OAuthUser.avatar,
        OAuthUser.phone_number,
        OAuthUser.openid,
        OAuthUser.appid,
        OAuthUser.create_time,
        OAuthUser.update_time,
    ]
    ordering = [OAuthUser.id.desc()]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(User, User.id == OAuthUser.user_id)


class OAuthUserLoginHistoryAdmin(ReadOnlyModelAdmin):
    page_schema = amis.PageSchema(label="授权记录", icon="fa fa-history")
    model = OAuthHistory
    ordering = [OAuthHistory.id.desc()]
    search_fields = [User.username, User.nickname]
    list_display = [
        OAuthHistory.id,
        User.username,
        User.nickname,
        OAuthHistory.ip,
        OAuthHistory.client,
        OAuthHistory.create_time,
    ]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(User, OAuthHistory.user_id == User.id)
