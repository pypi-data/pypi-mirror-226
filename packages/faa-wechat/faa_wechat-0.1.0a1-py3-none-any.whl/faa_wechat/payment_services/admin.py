from fastapi_amis_admin import admin, amis

from .models import PayService


class PayServiceAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label="付费服务", icon="fa fa-usd")
    model = PayService
    search_fields = [PayService.name]
    list_display = [
        PayService.id,
        PayService.name,
        PayService.price,
        PayService.value,
        PayService.desc,
        PayService.type,
        # PayService.img,
        PayService.create_time,
        PayService.is_active,
        PayService.sort,
    ]
    update_exclude = {"id", "create_time", "update_time"}
    create_fields = [
        PayService.name,
        PayService.price,
        PayService.value,
        PayService.desc,
        PayService.type,
        PayService.content,
        PayService.img,
    ]
