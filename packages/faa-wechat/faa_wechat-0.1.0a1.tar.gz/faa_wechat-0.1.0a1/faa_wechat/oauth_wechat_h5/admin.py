from fastapi_amis_admin import amis
from fastapi_config import ConfigAdmin

from .config import WxOAuthCfg


class WxOAuthCfgAdmin(ConfigAdmin):
    page_schema = amis.PageSchema(label="微信公众号配置", icon="fa fa-cogs")
    schema = WxOAuthCfg
