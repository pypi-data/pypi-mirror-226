from fastapi_amis_admin import amis
from fastapi_config import ConfigAdmin

from .config import WxAppletCfg


class WxAppletCfgAdmin(ConfigAdmin):
    page_schema = amis.PageSchema(label="微信小程序配置", icon="fa fa-cogs")
    schema = WxAppletCfg
