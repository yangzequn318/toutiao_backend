# -*- coding: utf-8 -*-
import json
from typing import Any, Optional

# FastAPI 是异步框架，必须使用 redis 自带的异步客户端，
# 否则同步的网络读写会直接阻塞整个事件循环，导致所有页面/接口卡死转圈
import redis.asyncio as aioredis

from config import settings

# 全局唯一的异步连接客户端（懒加载单例），不要每次请求都 new 一个
_redis_client: Optional["aioredis.Redis"] = None


def get_redis_client() -> "aioredis.Redis":
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=settings.REDIS_TIMEOUT,
            socket_timeout=settings.REDIS_TIMEOUT,
        )
    return _redis_client


# 读取：字符串
async def get_cache(key: str):
    try:
        return await get_redis_client().get(key)
    except Exception as e:
        print(f"获取缓存失败：{e}")
        return None


# 读取json
async def get_json_cache(key: str):
    try:
        data = await get_redis_client().get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"读取json缓存失败：{e}")
        return None


# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        await get_redis_client().setex(key, expire, value)
        return True
    except Exception as e:
        print(f"写入缓存失败：{e}")
        return False
