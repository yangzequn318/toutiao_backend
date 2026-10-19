# -*- coding: utf-8 -*-
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 密码加密
def get_hash_password(password: str):
    # bcrypt限制最多72字节，提前截断
    password_bytes = password.encode("utf-8")[:72]
    password_truncated = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(password_truncated)

# 密码验证: verify 返回值是布尔型
def verify_password(plain_password: str, hashed_password: str):
    # 登录校验也要同样截断，否则注册/登录逻辑不一致
    plain_bytes = plain_password.encode("utf-8")[:72]
    plain_truncated = plain_bytes.decode("utf-8", errors="ignore")
    return pwd_context.verify(plain_truncated, hashed_password)
