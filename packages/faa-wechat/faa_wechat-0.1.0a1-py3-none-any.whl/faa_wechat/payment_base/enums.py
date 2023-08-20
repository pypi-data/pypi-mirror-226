from fastapi_amis_admin import models


class PayCardStatus(models.IntegerChoices):
    """充值卡状态"""

    UNUSED = 1, "未使用"
    USED = 2, "已使用"
    SOLD = 3, "已出售"


class PayLogType(models.IntegerChoices):
    """支付日志类型"""

    RECHARGE = 1, "充值"
    CONSUME = 2, "消费"
    GIFT = 3, "赠送"
    REFUND = 4, "退款"


class PayType(models.IntegerChoices):
    """支付类型"""

    WXPAY = 1, "微信"
    ALIPAY = 2, "支付宝"
    UNIONPAY = 3, "银联"
    BALANCE = 4, "余额"
    OTHER = 5, "其他"


# 消费日志状态
class PayLogStatus(models.IntegerChoices):
    """推广收益处理状态"""

    WAIT = 1, "待处理"
    SUCCESS = 2, "成功"
    FAIL = 3, "失败"


class PayOrderStatus(models.IntegerChoices):
    """支付订单状态"""

    UNPAID = 1, "待支付"
    PAID = 2, "支付成功"
    CANCELED = 3, "已取消"
    REFUNDED = 4, "已退款"
    COMPLETED = 5, "已完成"
    # FAILED = 2, "发货失败"


class OrderType(models.TextChoices):
    """支付订单类型"""

    RECHARGE = "recharge", "余额充值"
    SERVICE = "service", "服务购买"


class ErrorCode(models.IntegerChoices):
    """错误代码"""

    # 数据异常
    INVALID_SIGNATURE = 41000, "签名错误"
    OPENID_NOT_FOUND = 41001, "openid不存在"

    # 订单相关
    CREATE_ORDER_ERROR = 42000, "生成订单失败"
    ORDER_TYPE_ERROR = 42001, "订单类型错误"
    ORDER_STATUS_ERROR = 42002, "订单状态错误"
    ORDER_NOT_FOUND = 42003, "订单不存在"
    ORDER_NOT_PAID = 42004, "订单未支付"
    ORDER_PAID = 42005, "订单已支付"
    ORDER_CANCELED = 42006, "订单已取消"
    ORDER_REFUNDED = 42007, "订单已退款"
    ORDER_COMPLETED = 42008, "订单已完成"
    ORDER_FAILED = 42009, "订单支付失败"
    ORDER_NOT_REFUNDABLE = 42010, "订单不可退款"
    ORDER_NOT_CANCELABLE = 42011, "订单不可取消"
    ORDER_NOT_COMPLETABLE = 42012, "订单不可完成"
    ORDER_NOT_PAID_OR_FAILED = 42014, "订单不可支付或失败"

    # 账号相关

    BALANCE_NOT_ENOUGH = 43000, "账号余额不足"
    ACCOUNT_NOT_FOUND = 43001, "账号不存在"
    ACCOUNT_ERROR = 43002, "账号异常"
    ACCOUNT_DISABLED = 43003, "账号已被禁用"
    ACCOUNT_LOCKED = 43004, "账号已被锁定"
    ACCOUNT_NOT_ACTIVATED = 43005, "账号未激活"
    ACCOUNT_NOT_BIND_WX = 43006, "账号未绑定微信"
    ACCOUNT_NOT_BIND_ALIPAY = 43007, "账号未绑定支付宝"
    ACCOUNT_SCORE_NOT_ENOUGH = 43008, "账号积分不足"

    # 服务相关
    SERVICE_NOT_FOUND = 44000, "服务不存在"
    SERVICE_OFF_SALE = 44001, "服务已下架"
    SERVICE_SOLD_OUT = 44002, "服务已售罄"
    SERVICE_NOT_PURCHASABLE = 44003, "服务不可购买"
    SERVICE_BOUGHT = 44004, "服务已购买"
    SERVICE_NOT_BOUGHT = 44005, "服务未购买"
    SERVICE_NOT_EXPIRED = 44006, "服务未过期"
    SERVICE_EXPIRED = 44007, "服务已过期"
    SERVICE_BUY_FAILED = 44008, "服务购买失败"
    SERVICE_TYPE_ERROR = 44009, "服务类型错误"


class WxPayType(models.IntegerChoices):
    """微信支付类型"""

    JSAPI = 0, "公众号支付"
    # APP = 1, "APP支付"
    H5 = 2, "H5支付"
    # NATIVE = 3, "扫码支付"
    MINIPROG = 4, "小程序支付"
