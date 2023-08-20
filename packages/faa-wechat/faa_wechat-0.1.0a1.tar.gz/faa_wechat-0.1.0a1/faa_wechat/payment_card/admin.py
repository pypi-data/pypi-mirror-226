from fastapi_amis_admin import admin, amis
from fastapi_user_auth.auth.models import User
from sqlalchemy.sql import Select
from starlette.requests import Request

from faa_wechat.payment_card.models import PayCard


class PayCardAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label="充值卡", icon="fa fa-folder")
    model = PayCard
    search_fields = [PayCard.sid]
    list_display = [
        PayCard.id,
        PayCard.sid,
        PayCard.value,
        PayCard.status,
        PayCard.creator_id,
        User.username,
        PayCard.create_time,
        PayCard.update_time,
    ]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(User, User.id == PayCard.user_id)
