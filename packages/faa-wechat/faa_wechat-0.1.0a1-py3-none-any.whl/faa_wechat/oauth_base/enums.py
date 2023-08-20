from fastapi_amis_admin import models


class OAuthType(models.IntegerChoices):
    """授权类型"""

    JSAPI = 0, "微信公众号"
    H5 = 2, "微信H5"
    APPLET = 4, "微信小程序"
    # github = "github", "Github"
    # google = "google", "Google"
    # qq = "qq", "QQ"
    # weibo = "weibo", "Weibo"


class OAuthErrorCode(models.IntegerChoices):
    # 微信授权错误码
    CODE_ERROR = (41000, "code无效")
    SESSION_KEY_ERROR = (41001, "session_key无效")
    ACCESS_TOKEN_ERROR = (41002, "access_token无效")
    OPENID_ERROR = (41003, "openid无效")
    USER_NOT_FOUND = (41004, "用户不存在")
    UPDATE_USER_INFO_ERROR = (41005, "更新用户信息失败,请登录重试!")
