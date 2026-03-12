# 自定義 HTTP 處理程序 (Custom HTTP Handler)

在 LiteLLM 完成 (completions) 中配置自定義 aiohttp 會話，以獲得更好的性能和控制。

## 概述 (Overview)

您現在可以將自定義 `aiohttp.ClientSession` 實例注入 LiteLLM，用於：
- 自定義連接池和超時 (timeouts)
- 企業代理 (corporate proxy) 和 SSL 配置  
- 性能優化
- 請求監控

## 基本用法 (Basic Usage)

### 預設 (無需更改)
```python
import litellm

# 與以前完全一樣
response = await litellm.acompletion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### 自定義會話 (Custom Session)
```python
import aiohttp
import litellm
from litellm.llms.custom_httpx.aiohttp_handler import BaseLLMAIOHTTPHandler

# 建立優化會話
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=180),
    connector=aiohttp.TCPConnector(limit=300, limit_per_host=75)
)

# 替換全域處理程序
litellm.base_llm_aiohttp_handler = BaseLLMAIOHTTPHandler(client_session=session)

# 所有完成現在都使用您的會話
response = await litellm.acompletion(model="gpt-3.5-turbo", messages=[...])
```

## 常見模式 (Common Patterns)

### FastAPI 整合
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiohttp
import litellm

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動 (Startup)
    session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=180),
        connector=aiohttp.TCPConnector(limit=300)
    )
    litellm.base_llm_aiohttp_handler = BaseLLMAIOHTTPHandler(
        client_session=session
    )
    yield
    # 關閉 (Shutdown)
    await session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/chat")
async def chat(messages: list[dict]):
    return await litellm.acompletion(model="gpt-3.5-turbo", messages=messages)
```

### 企業代理 (Corporate Proxy)
```python
import ssl

# 自定義 SSL 上下文
ssl_context = ssl.create_default_context()
ssl_context.load_cert_chain('cert.pem', 'key.pem')

# 代理會話
session = aiohttp.ClientSession(
    connector=aiohttp.TCPConnector(ssl=ssl_context),
    trust_env=True  # 使用環境代理設置
)

litellm.base_llm_aiohttp_handler = BaseLLMAIOHTTPHandler(client_session=session)
```

### 高性能 (High Performance)
```python
# 針對高吞吐量進行優化
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=300),
    connector=aiohttp.TCPConnector(
        limit=1000,             # 高連接限制
        limit_per_host=200,     # 每個主機限制
        ttl_dns_cache=600,      # DNS 快取
        keepalive_timeout=60,   # 保持連接活動
        enable_cleanup_closed=True
    )
)

litellm.base_llm_aiohttp_handler = BaseLLMAIOHTTPHandler(client_session=session)
```

## 建構函式選項 (Constructor Options)

```python
BaseLLMAIOHTTPHandler(
    client_session=None,    # 自定義 aiohttp.ClientSession
    transport=None,         # 高級傳輸控制
    connector=None,         # 自定義 aiohttp.BaseConnector
)
```

## 資源管理 (Resource Management)

- **用戶會話 (User sessions)**：由您管理生命週期（呼叫 `await session.close()`）
- **自動建立的會話 (Auto-created sessions)**：由處理程序自動清理
- **100% 回溯相容**：現有程式碼無需更改即可運行

## 配置提示 (Configuration Tips)

### 開發 (Development)
```python
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=60),
    connector=aiohttp.TCPConnector(limit=50)
)
```

### 生產 (Production)
```python
session = aiohttp.ClientSession(
    timeout=aiohttp.ClientTimeout(total=300),
    connector=aiohttp.TCPConnector(
        limit=1000,
        limit_per_host=200,
        keepalive_timeout=60
    )
)
```
