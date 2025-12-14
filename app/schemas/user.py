from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

class LoginType(str, Enum):
    ACCOUNT = "account"
    WECHAT = "wechat"
    DINGTALK = "dingtalk"
    QQ = "qq"
    PHONE = "phone"

class LoginDTO(BaseModel):
    login_type: LoginType = Field(..., description="登录类型: account, wechat, dingtalk, qq, phone")
    username: Optional[str] = Field(None, description="用户名/手机号 (account/phone模式必填)")
    password: Optional[str] = Field(None, description="密码 (account模式必填)")
    code: Optional[str] = Field(None, description="授权码/验证码 (wechat/dingtalk/qq/phone模式必填)")

class LoginVO(BaseModel):
    token: str = Field(..., description="Token")
    message: str = Field(..., description="消息")
    userInfo: Optional[dict] = Field(None, description="用户信息")
