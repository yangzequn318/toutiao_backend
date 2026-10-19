# -*- coding: utf-8 -*-
"""
项目集中配置入口
从 .env 文件或系统环境变量读取，未配置时使用合理的开发默认值
"""
import os
from typing import Optional

# 加载项目根目录的 .env 文件（如果存在）
try:
    from dotenv import load_dotenv
    # 默认 .env 在项目根目录（本文件在 config/ 下）
    _ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    load_dotenv(_ENV_PATH, override=False)
except ImportError:
    pass  # 没装 python-dotenv 时回退到系统环境变量


def _get_int(key: str, default: int) -> int:
    v = os.environ.get(key)
    if v is None:
        return default
    try:
        return int(v)
    except ValueError:
        return default


# ============ 数据库（MySQL） ============
DB_HOST: str = os.environ.get("DB_HOST", "localhost")
DB_PORT: int = _get_int("DB_PORT", 3306)
DB_USER: str = os.environ.get("DB_USER", "root")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
DB_NAME: str = os.environ.get("DB_NAME", "news_app")
DB_CHARSET: str = os.environ.get("DB_CHARSET", "utf8mb4")

# 允许直接覆盖完整 URL（优先级高于上面各字段）
_DATABASE_URL_OVERRIDE: Optional[str] = os.environ.get("DATABASE_URL")

if _DATABASE_URL_OVERRIDE:
    ASYNC_DATABASE_URL: str = _DATABASE_URL_OVERRIDE
else:
    # aiomysql 的驱动前缀：mysql+aiomysql
    ASYNC_DATABASE_URL = (
        f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"
    )

DB_ECHO_SQL: bool = os.environ.get("DB_ECHO_SQL", "true").lower() in ("1", "true", "yes", "on")
DB_POOL_SIZE: int = _get_int("DB_POOL_SIZE", 10)
DB_MAX_OVERFLOW: int = _get_int("DB_MAX_OVERFLOW", 20)


# ============ Redis 缓存 ============
REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT: int = _get_int("REDIS_PORT", 6379)
REDIS_DB: int = _get_int("REDIS_DB", 0)
REDIS_PASSWORD: Optional[str] = os.environ.get("REDIS_PASSWORD") or None
REDIS_TIMEOUT: int = _get_int("REDIS_TIMEOUT", 2)


# ============ 应用 ============
APP_HOST: str = os.environ.get("APP_HOST", "127.0.0.1")
APP_PORT: int = _get_int("APP_PORT", 8000)


def __repr__() -> str:
    """仅用于调试打印时遮蔽密码"""
    return (
        f"Settings("
        f"DB_HOST={DB_HOST!r}, DB_PORT={DB_PORT}, DB_USER={DB_USER!r}, "
        f"DB_PASSWORD={'*' * (len(DB_PASSWORD) if DB_PASSWORD else 0)}, "
        f"DB_NAME={DB_NAME!r}, ASYNC_DATABASE_URL={ASYNC_DATABASE_URL!r}, "
        f"REDIS_HOST={REDIS_HOST!r}, REDIS_PORT={REDIS_PORT}, REDIS_DB={REDIS_DB}, "
        f"REDIS_PASSWORD={'*' * (len(REDIS_PASSWORD) if REDIS_PASSWORD else 0)}, "
        f"DB_ECHO_SQL={DB_ECHO_SQL}"
        f")"
    )
