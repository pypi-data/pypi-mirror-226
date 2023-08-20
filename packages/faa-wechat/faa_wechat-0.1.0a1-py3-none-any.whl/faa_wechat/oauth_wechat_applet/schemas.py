from fastapi_amis_admin.models import Field
from pydantic import BaseModel


class WxEncryptedData(BaseModel):
    iv: str = Field(..., title="加密算法的初始向量")
    encrypted_data: str = Field(..., alias="encryptedData", title="包括敏感数据在内的完整用户信息的加密数据")
