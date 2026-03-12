# 用於 LiteLLM 的 Braintrust 提示詞包裝器 (Prompt Wrapper)

此目錄包含一個包裝器伺服器，使 LiteLLM 能夠透過通用提示管理 API 使用來自 [Braintrust](https://www.braintrust.dev/) 的提示詞。

## 架構

```
┌─────────────┐         ┌──────────────────────┐         ┌─────────────┐
│   LiteLLM   │ ──────> │  包裝器伺服器        │ ──────> │  Braintrust │
│   用戶端    │         │  (本伺服器)          │         │     API     │
└─────────────┘         └──────────────────────┘         └─────────────┘
    使用通用                 轉換格式                      儲存實際的
    提示管理員             從 Braintrust 格式              提示詞範本
                         轉換為 LiteLLM 格式
```

## 組件

### 1. 通用提示管理員 (`litellm/integrations/generic_prompt_management/`)

一個通用的用戶端，可與任何實作了 `/beta/litellm_prompt_management` 端點的 API 配合使用。

**預期的 API 回應格式：**
```json
{
  "prompt_id": "string",
  "prompt_template": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello {name}"}
  ],
  "prompt_template_model": "gpt-4",
  "prompt_template_optional_params": {
    "temperature": 0.7,
    "max_tokens": 100
  }
}
```

### 2. Braintrust 包裝器伺服器 (`braintrust_prompt_wrapper_server.py`)

一個 FastAPI 伺服器，負責：
- 實作 `/beta/litellm_prompt_management` 端點
- 從 Braintrust API 獲取提示詞
- 將 Braintrust 回應格式轉換為 LiteLLM 格式

## 設定

### 安裝依賴

```bash
pip install fastapi uvicorn httpx litellm
```

### 設定環境變數

```bash
export BRAINTRUST_API_KEY="your-braintrust-api-key"
```

## 使用方法

### 步驟 1：啟動包裝器伺服器

```bash
python braintrust_prompt_wrapper_server.py
```

伺服器預設將在 `http://localhost:8080` 啟動。

您可以自定義連接埠與主機：
```bash
export PORT=8000
export HOST=0.0.0.0
python braintrust_prompt_wrapper_server.py
```

### 步驟 2：與 LiteLLM 配合使用

```python
import litellm
from litellm.integrations.generic_prompt_management import GenericPromptManager

# 配置通用提示管理員以使用您的包裝器伺服器
generic_config = {
    "api_base": "http://localhost:8080",
    "api_key": "your-braintrust-api-key",  # 將傳遞給 Braintrust
    "timeout": 30,
}

# 建立提示管理員
prompt_manager = GenericPromptManager(**generic_config)

# 搭配 completion 使用
response = litellm.completion(
    model="generic_prompt/gpt-4",
    prompt_id="your-braintrust-prompt-id",
    prompt_variables={"name": "World"},  # 要替換的變數
    messages=[{"role": "user", "content": "Additional message"}]
)

print(response)
```

### 步驟 3：直接進行 API 測試

您也可以直接測試包裝器 API：

```bash
# 使用 curl 測試
curl -H "Authorization: Bearer YOUR_BRAINTRUST_TOKEN" \
     "http://localhost:8080/beta/litellm_prompt_management?prompt_id=YOUR_PROMPT_ID"

# 健康檢查
curl http://localhost:8080/health

# 服務資訊
curl http://localhost:8080/
```

## API 文件

伺服器啟動後，請造訪：
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Braintrust 格式轉換

包裝器會自動轉換 Braintrust 的回應格式：

**Braintrust API 回應：**
```json
{
  "id": "prompt-123",
  "prompt_data": {
    "prompt": {
      "type": "chat",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant"
        }
      ]
    },
    "options": {
      "model": "..."
    }
  }
}
```
*(以此類推，轉換為上述 LiteLLM 預期格式)*
