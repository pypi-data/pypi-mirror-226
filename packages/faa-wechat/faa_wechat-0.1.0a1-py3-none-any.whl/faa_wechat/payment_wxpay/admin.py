from fastapi_amis_admin import amis
from fastapi_config import ConfigAdmin

from .config import WxPayCfg


class WxPayCfgAdmin(ConfigAdmin):
    page_schema = amis.PageSchema(label="微信支付配置", icon="fa fa-cogs")
    schema = WxPayCfg
