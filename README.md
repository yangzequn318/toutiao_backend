# 📰 头条新闻后端（HeadlineNews API）

一个基于 **FastAPI** + **MySQL** + **Redis** 的头条新闻类内容聚合平台后端服务，提供新闻浏览、用户体系、收藏、浏览历史等 RESTful API。

> 项目定位：作为前端头条新闻应用的后端支撑，完整覆盖「内容 → 用户 → 交互」三大模块，集成 Redis 缓存优化热点接口。

---

## ✨ 功能概览

| 模块 | 能力 |
|---|---|
| 📰 **新闻内容** | 分类查询、新闻列表分页、新闻详情（含浏览量自增、相关推荐） |
| 👤 **用户体系** | 注册 / 登录、用户资料查询与更新、密码修改、Token 鉴权 |
| ⭐ **收藏夹** | 收藏 / 取消收藏、批量检查、收藏列表、一键清空 |
| 🕑 **浏览历史** | 自动记录、历史列表、单条/批量删除 |
| ⚡ **Redis 缓存** | 分类热点数据、新闻列表、详情、相关推荐均走缓存 → 回源数据库 |
| 🔐 **密码安全** | 使用 bcrypt 加盐哈希存储，不复用明文 |

---

## 🧱 技术栈

| 层级 | 技术 | 版本 | 说明 |
|---|---|---|---|
| Web 框架 | FastAPI | 0.141 | 现代、异步、自动生成 Swagger 文档 |
| ASGI 服务器 | Uvicorn | 0.54 | 生产级异步服务器，支持热重载 |
| ORM | SQLAlchemy | 2.1 | 异步 ORM，连接池管理 |
| 数据库 | MySQL | — | aiomysql 异步驱动 |
| 缓存 | Redis | — | redis.asyncio 异步客户端，全局单例连接池 |
| 数据校验 | Pydantic v2 | 2.13 | 请求/响应模型定义与校验 |
| 配置管理 | python-dotenv | 1.2 | 从 `.env` 加载敏感配置，代码零硬编码 |
| 密码安全 | passlib + bcrypt | — | bcrypt 加盐哈希 |

---

## 🗂️ 项目结构

```
toutiao_backend/
├── main.py                  # 应用入口，注册全局中间件与路由
├── requirements.txt         # Python 依赖清单
├── .env.example             # 环境变量模板（复制为 .env 使用）
├── .gitignore               # Git 忽略规则（排除 .env / .venv / __pycache__ 等）
│
├── config/                  # ⚙️ 配置层
│   ├── settings.py          # 统一配置入口（.env → 类型化常量）
│   ├── db_conf.py           # MySQL 异步引擎 / 会话工厂
│   └── cache_conf.py        # Redis 异步客户端（全局单例 + 2s 超时保护）
│
├── routers/                 # 🚏 路由层（API 入口）
│   ├── news.py              # /api/news/*   新闻内容
│   ├── users.py             # /api/user/*   用户体系
│   ├── favorite.py          # /api/favorite/* 收藏
│   └── history.py           # /api/history/* 浏览历史
│
├── crud/                    # 💾 数据访问层（SQLAlchemy 查询封装）
│   ├── news.py              # 新闻相关 DB 操作
│   ├── news_cache.py        # 新闻相关「缓存 → DB 回源」双写策略
│   ├── users.py
│   ├── favorite.py
│   └── history.py
│
├── cache/                   # 🗃️ Redis 缓存封装（key 命名、过期时间、双写策略）
│   └── news_cache.py        # 分类 7200s / 列表 1800s / 详情 300s / 相关推荐 1800s
│
├── models/                  # 📐 数据库 ORM 模型（基于 SQLAlchemy 2.0 declarative）
├── schemas/                 # 📝 Pydantic 请求/响应模型（与前端字段对齐）
└── utils/                   # 🛠️ 工具库
    ├── auth.py              # Token 鉴权依赖（FastAPI Depends）
    ├── security.py          # bcrypt 哈希封装
    ├── exception.py         # 自定义异常
    ├── exception_handlers.py# 全局异常处理器
    └── response.py          # 统一响应格式辅助
```

---

## 🚀 快速开始

### 前置条件

- Python **3.10+**
- MySQL **5.7+**（或 8.x），创建数据库 `news_app`
- Redis **6.x+**

### 1. 克隆并安装依赖

```bash
cd toutiao_backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

编辑 `.env`，填入你本机 MySQL / Redis 的真实密码：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的真实密码       # ⚠️  千万别提交到 Git！
DB_NAME=news_app
DB_ECHO_SQL=false
```

> 💡 `.env` 已被 `.gitignore` 排除，不会进入版本控制。

### 3. 启动 MySQL 与 Redis

MySQL 中确保 `news_app` 数据库存在，表结构由 ORM 的 SQLAlchemy 模型定义（需你自己根据 `models/` 目录建表，或使用 Alembic 迁移）。

### 4. 启动服务

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- 服务启动后自动监听 `http://127.0.0.1:8000`
- 内置 CORS 中间件，前端可直接跨域调用
- Swagger 交互式文档：`http://127.0.0.1:8000/docs`
- ReDoc 文档：`http://127.0.0.1:8000/redoc`

---

## 🔌 API 接口一览

### 📰 新闻 `/api/news`

| 方法 | 路径 | 参数 | 说明 |
|---|---|---|---|
| GET | `/categories` | `skip`, `limit` | 获取所有新闻分类 |
| GET | `/list` | `categoryId`, `page`, `pageSize` | 新闻列表分页（带 Redis 缓存） |
| GET | `/detail` | `id` | 新闻详情（浏览量 +1 + 相关推荐） |

### 👤 用户 `/api/user`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/register` | 用户注册 |
| POST | `/login` | 用户登录，返回 Token |
| GET | `/info` | 获取当前登录用户信息 |
| PUT | `/update` | 更新用户资料 |
| PUT | `/password` | 修改密码 |

### ⭐ 收藏 `/api/favorite`

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/check` | 检查某条新闻是否已收藏 |
| POST | `/add` | 添加收藏 |
| DELETE | `/remove` | 取消收藏 |
| GET | `/list` | 当前用户的收藏列表 |
| DELETE | `/clear` | 一键清空收藏 |

### 🕑 历史 `/api/history`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/add` | 添加一条浏览记录 |
| GET | `/list` | 当前用户的浏览历史列表 |
| DELETE | `/delete/{history_id}` | 删除单条历史 |
| DELETE | `/clear` | 清空浏览历史 |

> 所有需要登录的接口通过 Header `Authorization: Bearer <token>` 传递身份令牌。

---

## 🏆 项目亮点

1. **全异步技术栈** — FastAPI + aiomysql + redis.asyncio + SQLAlchemy AsyncEngine，事件循环零阻塞。
2. **缓存穿透 / 雪崩防护** — Redis 全局单例连接池 + 2s 超时保护，Redis 挂了立即回源 DB，不会拖垮整个服务。
3. **分层架构清晰** — `routers` → `crud` → `models`，职责分明；缓存与 DB 查询分离在 `crud/news_cache.py`。
4. **敏感信息零硬编码** — 密码、URL、端口全部抽入 `.env`，代码仓库里找不到任何真实凭据。
5. **可复现部署** — `.env.example` + `requirements.txt` + README，他人拿到即可本地跑起来。
6. **智能缓存策略** — 热点接口走缓存，且根据数据稳定性差异化设置 TTL（分类 2h、列表 30min、详情 5min）。

---

## 🛡️ 安全说明

| 风险点 | 处理方式 |
|---|---|
| 数据库密码硬编码 | ✅ 已迁移到 `.env`，`.env` 被 `.gitignore` 排除 |
| Redis 密码硬编码 | ✅ 同上，支持通过 `.env` 配置 |
| 用户密码明文存储 | ✅ 使用 bcrypt 加盐哈希 |
| CORS 跨域 | ✅ 生产环境应收紧 `allow_origins`（当前为 `*`，开发友好） |
| Token 鉴权 | ✅ 使用服务端生成的 UUID Token + 过期时间 |

---

## 📁 相关链接

- FastAPI 官方文档：https://fastapi.tiangolo.com/
- SQLAlchemy Async：https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Redis 异步客户端：https://redis-py.readthedocs.io/en/stable/examples/asyncio_examples.html

---

## 📄 License

MIT
