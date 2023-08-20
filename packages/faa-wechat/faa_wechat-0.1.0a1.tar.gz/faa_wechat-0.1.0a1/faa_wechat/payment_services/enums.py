from fastapi_amis_admin import models


# 服务类型
class ServiceType(models.TextChoices):
    """服务类型"""

    VIP = "vip", "VIP开通"
    # 充值
    RECHARGE = "recharge", "余额充值"
