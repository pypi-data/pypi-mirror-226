from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.admin import AdminApp
from fastapi_amis_admin.amis import TableColumn
from fastapi_user_auth.auth.models import User
from fastapi_user_auth.mixins.admin import ReadOnlyModelAdmin
from pydantic.fields import ModelField
from sqlalchemy.sql import Select
from starlette.requests import Request

from faa_wechat.oauth_base.models import OAuthUser
from faa_wechat.payment_base.models import BalanceLog, PayOrder, ScoreLog


class PaymentApp(admin.AdminApp):
    page_schema = amis.PageSchema(label="支付系统", icon="fa fa-paypal")
    router_prefix = "/payment"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(
            PayOrderAdmin,
            PayBalanceLogAdmin,
            PayScoreLogAdmin,
            # PayCardAdmin,
        )


class PayOrderAdmin(ReadOnlyModelAdmin):
    page_schema = amis.PageSchema(label="支付订单", icon="fa fa-list")
    model = PayOrder
    search_fields = [OAuthUser.nickname]
    readonly_fields = [PayOrder.trade_no, PayOrder.openid]
    list_display = [
        OAuthUser.user_id,
        PayOrder.pay_type,
        PayOrder.total_fee,
        PayOrder.status,
        PayOrder.body,
        PayOrder.trade_no,
        OAuthUser.nickname,
        PayOrder.create_time,
        PayOrder.pay_time,
        PayOrder.attach,
    ]
    ordering = [PayOrder.id.desc()]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(OAuthUser, OAuthUser.openid == PayOrder.openid)

    async def get_list_column(self, request: Request, modelfield: ModelField) -> TableColumn:
        column = await super().get_list_column(request, modelfield)
        # 默认不显示 trade_no
        if modelfield.name in {"attach"}:
            column.toggled = False
        return column

    # async def get_actions_on_item(self, request: Request) -> List[Action]:
    #     actions = await super().get_actions_on_item(request)
    #     actions.append(
    #         ActionType.Ajax(
    #             label="查询支付结果",
    #             api=f"get:{self.router_path}/query_order?trade_no=$trade_no",
    #         )
    #     )
    #     return actions
    #
    # def register_router(self):
    #     super().register_router()
    #
    #     # 查询支付结果API
    #     @self.router.get("/query_order", summary="查询支付结果")
    #     async def query_order(request: Request, trade_no: str):
    #         result = await self.db.async_run_sync(query_and_complete_order, trade_no)
    #         return result
    #
    #     return self


class PayBalanceLogAdmin(ReadOnlyModelAdmin):
    page_schema = amis.PageSchema(label="消费日志", icon="fa fa-yen")
    model = BalanceLog
    search_fields = [User.username]
    list_display = [
        BalanceLog.id,
        BalanceLog.user_id,
        User.username,
        BalanceLog.type,
        BalanceLog.value,
        BalanceLog.value1,
        BalanceLog.desc,
        BalanceLog.create_time,
    ]
    ordering = [BalanceLog.id.desc()]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(User, User.id == BalanceLog.user_id)


class PayScoreLogAdmin(ReadOnlyModelAdmin):
    page_schema = amis.PageSchema(label="积分日志", icon="fa fa-yen")
    model = ScoreLog
    search_fields = [User.username]
    list_display = [
        ScoreLog.id,
        ScoreLog.user_id,
        User.username,
        ScoreLog.type,
        ScoreLog.value,
        ScoreLog.value1,
        ScoreLog.desc,
        ScoreLog.create_time,
    ]
    ordering = [ScoreLog.id.desc()]

    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.outerjoin(User, User.id == ScoreLog.user_id)
