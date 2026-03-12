# liteLLM Proxy Server：支援 50+ 種 LLM 模型、錯誤處理與快取

### Azure, Llama2, OpenAI, Claude, Hugging Face, Replicate 模型

[![PyPI Version](https://img.shields.io/pypi/v/litellm.svg)](https://pypi.org/project/litellm/)
[![PyPI Version](https://img.shields.io/badge/stable%20version-v0.1.345-blue?color=green&link=https://pypi.org/project/litellm/0.1.1/)](https://pypi.org/project/litellm/0.1.1/)
![Downloads](https://img.shields.io/pypi/dm/litellm)
[![litellm](https://img.shields.io/badge/%20%F0%9F%9A%85%20liteLLM-OpenAI%7CAzure%7CAnthropic%7CPalm%7CCohere%7CReplicate%7CHugging%20Face-blue?color=green)](https://github.com/BerriAI/litellm)

[![在 Railway 上部署](https://railway.app/button.svg)](https://railway.app/template/DYqQAW?referralCode=t3ukrU)

![4BC6491E-86D0-4833-B061-9F54524B2579](https://github.com/BerriAI/litellm/assets/17561003/f5dd237b-db5e-42e1-b1ac-f05683b1d724)

## liteLLM Proxy 的功能

- 針對 50+ 種 LLM 模型發送 `/chat/completions` 請求，包括 **Azure, OpenAI, Replicate, Anthropic, Hugging Face**

  範例：`model` 可使用 `claude-2`, `gpt-3.5`, `gpt-4`, `command-nightly`, `stabilityai/stablecode-completion-alpha-3b-4k`

  ```json
  {
    "model": "replicate/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
    "messages": [
      {
        "content": "哈囉，舊金山的天氣如何？",
        "role": "user"
      }
    ]
  }
  ```

- **一致的輸入/輸出格式**
  - 使用 OpenAI 格式呼叫所有模型 - `completion(model, messages)`
  - 文字回應始終位於 `['choices'][0]['message']['content']`
- **錯誤處理** 使用模型回退 (Model Fallbacks) 機制（如果 `GPT-4` 失敗，則嘗試 `llama2`）
- **日誌紀錄** - 將請求、回應和錯誤紀錄至 `Supabase`, `Posthog`, `Mixpanel`, `Sentry`, `Lunary`, `Athina`, `Helicone`（支援此處列出的任何供應商：https://litellm.readthedocs.io/en/latest/advanced/）

  **範例：發送到 Supabase 的日誌**
  <img width="1015" alt="Screenshot 2023-08-11 at 4 02 46 PM" src="https://github.com/ishaan-jaff/proxy-server/assets/29436595/237557b8-ba09-4917-982c-8f3e1b2c8d08">

- **Token 使用量與支出** - 追蹤輸入 + 補全 Token 使用量以及每個模型的支出
- **快取** - 實作語義快取 (Semantic Caching)
- **串流與非同步支援** - 返回生成器以串流方式獲取文字回應

## API 端點

### `/chat/completions` (POST)

此端點用於為 50+ 種支援的 LLM API 模型產生對話補全。支援 llama2, GPT-4, Claude2 等。

#### 輸入

此 API 端點接受原始 JSON 格式的所有輸入，並預期以下欄位：

- `model` (string, 必填): 用於對話補全的模型 ID。請參閱[此處](https://litellm.readthedocs.io/en/latest/supported/)查看所有支援的模型：
  例如：`gpt-3.5-turbo`, `gpt-4`, `claude-2`, `command-nightly`, `stabilityai/stablecode-completion-alpha-3b-4k`
- `messages` (array, 必填): 代表對話內容的訊息清單。每條訊息應包含 `role`（system, user, assistant 或 function）和 `content`（訊息文字）。
