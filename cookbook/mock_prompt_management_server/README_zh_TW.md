# Mock Prompt Management Server

這是 [LiteLLM Generic Prompt Management API](https://docs.litellm.ai/docs/adding_provider/generic_prompt_management_api) 的參考實作。

此 FastAPI 伺服器展示了如何建立一個 prompt 管理 API 並與 LiteLLM 整合，且無需向 LiteLLM 儲存庫提交 PR。

## 快速上手

### 1. 安裝依賴項目

```bash
pip install fastapi uvicorn pydantic
```

### 2. 啟動伺服器

```bash
python mock_prompt_management_server.py
```

伺服器將在 `http://localhost:8080` 啟動。

### 3. 測試端點 (Endpoint)

```bash
# 取得一個 prompt
curl "http://localhost:8080/beta/litellm_prompt_management?prompt_id=hello-world-prompt"

# 使用身份驗證取得 prompt
curl "http://localhost:8080/beta/litellm_prompt_management?prompt_id=hello-world-prompt" \
  -H "Authorization: Bearer test-token-12345"

# 列出所有 prompts
curl "http://localhost:8080/prompts"

# 取得 prompt 變數
curl "http://localhost:8080/prompts/hello-world-prompt/variables"
```

## 與 LiteLLM 搭配使用

### 配置 (Configuration)

建立一個 `config.yaml` 檔案：

```yaml
model_list:
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY

prompts:
  - prompt_id: "hello-world-prompt"
    litellm_params:
      prompt_integration: "generic_prompt_management"
      api_base: http://localhost:8080
      api_key: test-token-12345
```

### 啟動 LiteLLM Proxy

```bash
litellm --config config.yaml
```

### 發送請求

```bash
curl http://0.0.0.0:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-1234" \
  -d '{
    "model": "gpt-3.5-turbo",
    "prompt_id": "hello-world-prompt",
    "prompt_variables": {
      "domain": "data science",
      "task": "analyzing customer behavior"
    },
    "messages": [
      {"role": "user", "content": "Please help me get started"}
    ]
  }'
```

## 可用的 Prompts

此伺服器包含多個範例 prompts：

| Prompt ID | 描述 | 變數 |
|-----------|-------------|-----------|
| `hello-world-prompt` | 基礎助手 | `domain`, `task` |
| `code-review-prompt` | 程式碼審查助手 | `years_experience`, `language`, `code` |
| `customer-support-prompt` | 客戶支援代理 | `company_name`, `customer_message` |
| `data-analysis-prompt` | 資料分析專家 | `analysis_type`, `dataset_name`, `data` |
| `creative-writing-prompt` | 創意寫作助手 | `genre`, `length`, `topic` |

## 身份驗證 (Authentication)

伺服器支援選用的 Bearer token 身份驗證。測試用的有效 tokens：

- `test-token-12345`
- `dev-token-67890`
- `prod-token-abcdef`

如果未提供 `Authorization` 標頭 (header)，則允許請求（僅用於測試目的）。

## API 端點 (Endpoints)

### LiteLLM Spec 端點

#### `GET /beta/litellm_prompt_management`

根據 ID 取得 prompt（LiteLLM 要求）。

**查詢參數 (Query Parameters):**
- `prompt_id` (必填): prompt ID
- `project_name` (選填): 專案過濾器
- `slug` (選填): Slug 過濾器
- `version` (選填): 版本過濾器

**回應 (Response):**
```json
{
  "prompt_id": "hello-world-prompt",
  "prompt_id": "hello-world-prompt",
  "prompt_template": [
    {
      "role": "system",
      "content": "You are a helpful assistant specialized in {domain}."
    },
    {
      "role": "user",
      "content": "Help me with: {task}"
    }
  ],
  "prompt_template_model": "gpt-4",
  "prompt_template_optional_params": {
    "temperature": 0.7,
    "max_tokens": 500
  }
}
```

### 便利端點 (不屬於 LiteLLM Spec)

#### `GET /health`

健康檢查 (Health check) 端點。

#### `GET /prompts`

列出所有可用的 prompts。

#### `GET /prompts/{prompt_id}/variables`

取得 prompt 模板中使用的所有變數。

#### `POST /prompts`

建立新的 prompt（僅儲存於記憶體，用於測試）。

## 範例：完整整合測試

### 1. 啟動 Mock 伺服器

```bash
python mock_prompt_management_server.py
```

### 2. 使用 Python 測試

```python
from litellm import completion

# 此 completion 將會：
# 1. 從您的 API 獲取 prompt
# 2. 將 {domain} 替換為 "machine learning"
# 3. 將 {task} 替換為 "building a recommendation system"
# 4. 與您的訊息 (messages) 合併
# 5. 使用 prompt 中指定的模型與參數

response = completion(
    model="gpt-4",
    prompt_id="hello-world-prompt",
    prompt_variables={
        "domain": "machine learning",
        "task": "building a recommendation system"
    },
    messages=[
        {"role": "user", "content": "I have user behavior data from the past year."}
    ],
    # 配置 generic prompt manager
    generic_prompt_config={
        "api_base": "http://localhost:8080",
        "api_key": "test-token-12345",
    }
)

print(response.choices[0].message.content)
```

## 客製化

### 新增 Prompts

編輯 `mock_prompt_management_server.py` 中的 `PROMPTS_DB` 字典：

```python
PROMPTS_DB = {
    "my-custom-prompt": {
        "prompt_id": "my-custom-prompt",
        "prompt_template": [
            {
                "role": "system",
                "content": "You are a {role}."
            },
            {
                "role": "user",
                "content": "{user_input}"
            }
        ],
        "prompt_template_model": "gpt-4",
        "prompt_template_optional_params": {
            "temperature": 0.8,
            "max_tokens": 1000
        }
    }
}
```

### 使用資料庫

將 `PROMPTS_DB` 字典替換為資料庫查詢：

```python
@app.get("/beta/litellm_prompt_management")
async def get_prompt(prompt_id: str):
    # 從資料庫獲取
    prompt = await db.prompts.find_one({"prompt_id": prompt_id})
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return PromptResponse(**prompt)
```

### 新增存取控制

使用自定義查詢參數進行存取控制：

```python
@app.get("/beta/litellm_prompt_management")
async def get_prompt(
    prompt_id: str,
    project_name: Optional[str] = None,
    user_id: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    token = verify_api_key(authorization)
    
    # 檢查使用者是否有權限存取此專案
    if not has_project_access(token, project_name):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # 獲取並回傳 prompt
    ...
```

## 生產環境考量

在部署到生產環境之前：

1. **使用真實資料庫**而非記憶體儲存
2. **實作完善的身份驗證**（使用 JWT tokens 或 API keys）
3. **加入速率限制 (rate limiting)** 以防止濫用
4. **使用 HTTPS** 進行加密通訊
5. **加入日誌與監控**以實現可觀測性 (observability)
6. **實作快取 (caching)** 以處理頻繁存取的 prompts
7. **加入版本控制**以便管理 prompts
8. **實作基於團隊/使用者的存取控制**
9. **為所有參數加入輸入驗證**
10. **使用環境變數**進行配置

## 相關文件

- [Generic Prompt Management API 文件](https://docs.litellm.ai/docs/adding_provider/generic_prompt_management_api)
- [LiteLLM Prompt 管理](https://docs.litellm.ai/docs/proxy/prompt_management)
- [Generic Guardrail API](https://docs.litellm.ai/docs/adding_provider/generic_guardrail_api)

## 有疑問嗎？

這是 LiteLLM Generic Prompt Management API 的參考實作。如有任何問題或建議，請在 [LiteLLM GitHub repository](https://github.com/BerriAI/litellm) 提交 issue。
