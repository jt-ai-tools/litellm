import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 批次完成 (Batching Completion)
LiteLLM 允許您：
* 向 1 個模型發送多個完成 (completion) 呼叫
* 向多個模型發送 1 個完成呼叫：返回最快的回應
* 向多個模型發送 1 個完成呼叫：返回所有回應

## 向 1 個模型發送多個完成呼叫

使用此功能並行處理請求。

<Tabs>
<TabItem value="sdk" label="SDK">

### 範例程式碼
```python
import litellm
import os

os.environ['OPENAI_API_KEY'] = ""

response = litellm.batch_completion(
    model="gpt-3.5-turbo",
    messages = [
        [
            {
                "role": "user",
                "content": "good morning"
            }
        ],
        [
            {
                "role": "user",
                "content": "what's the time? "
            }
        ]
    ]
)
```

</TabItem>
<TabItem value="proxy" label="PROXY">

1. 在 config.yaml 中定義模型

```yaml
model_list:
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 使用 OpenAI Python SDK 進行測試

```python
import openai
client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

# 向代理上設置的模型發送請求，`litellm --model`
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [
        [
            {
                "role": "user",
                "content": "good morning"
            }
        ],
        [
            {
                "role": "user",
                "content": "what's the time? "
            }
        ]
    ]
)
```

</TabItem>
</Tabs>

## 向多個模型發送 1 個完成呼叫：返回最快的回應
這會對指定的 `models` 進行並行呼叫，並返回第一個回應。

使用此功能可降低延遲。

<Tabs>
<TabItem value="sdk" label="SDK">

### 範例程式碼
```python
import litellm
import os
from litellm import batch_completion_models

os.environ['ANTHROPIC_API_KEY'] = ""
os.environ['OPENAI_API_KEY'] = ""
os.environ['COHERE_API_KEY'] = ""

response = batch_completion_models(
    models=["gpt-3.5-turbo", "claude-instant-1.2", "command-nightly"], 
    messages=[{"role": "user", "content": "Hey, how's it going"}]
)
print(result)
```



</TabItem>
<TabItem value="proxy" label="PROXY">

[如何設置代理配置](#example-setup)

只需傳遞以逗號分隔的模型名稱字串以及標記 `fastest_response=True`。

<Tabs>
<TabItem value="curl" label="curl">

```bash

curl -X POST 'http://localhost:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \ 
-D '{
    "model": "gpt-4o, groq-llama", # 👈 以逗號分隔的模型
    "messages": [
      {
        "role": "user",
        "content": "What's the weather like in Boston today?"
      }
    ],
    "stream": true,
    "fastest_response": true # 👈 標記
}

'
```

</TabItem>
<TabItem value="openai" label="OpenAI SDK">

```python
import openai
client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

# 向代理上設置的模型發送請求，`litellm --model`
response = client.chat.completions.create(
    model="gpt-4o, groq-llama", # 👈 以逗號分隔的模型
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ],
    extra_body={"fastest_response": true} # 👈 標記
)

print(response)
```

</TabItem>
</Tabs>

---

### 範例設置： 

```yaml 
model_list: 
- model_name: groq-llama
  litellm_params:
    model: groq/llama3-8b-8192
    api_key: os.environ/GROQ_API_KEY
- model_name: gpt-4o
  litellm_params:
    model: gpt-4o
    api_key: os.environ/OPENAI_API_KEY
```

```bash
litellm --config /path/to/config.yaml

# 運行於 http://0.0.0.0:4000
```

</TabItem>
</Tabs>

### 輸出 (Output)
返回 OpenAI 格式的第一個回應。取消其他 LLM API 呼叫。 
```json
{
  "object": "chat.completion",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": " I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, harmless, and honest.",
        "role": "assistant",
        "logprobs": null
      }
    }
  ],
  "id": "chatcmpl-23273eed-e351-41be-a492-bafcf5cf3274",
  "created": 1695154628.2076092,
  "model": "command-nightly",
  "usage": {
    "prompt_tokens": 6,
    "completion_tokens": 14,
    "total_tokens": 20
  }
}
```


## 向多個模型發送 1 個完成呼叫：返回所有回應
這會對指定的模型進行並行呼叫並返回所有回應。

使用此功能可並行處理請求並從多個模型獲取回應。

### 範例程式碼
```python
import litellm
import os
from litellm import batch_completion_models_all_responses

os.environ['ANTHROPIC_API_KEY'] = ""
os.environ['OPENAI_API_KEY'] = ""
os.environ['COHERE_API_KEY'] = ""

responses = batch_completion_models_all_responses(
    models=["gpt-3.5-turbo", "claude-instant-1.2", "command-nightly"], 
    messages=[{"role": "user", "content": "Hey, how's it going"}]
)
print(responses)

```

### 輸出 (Output)

```json
[<ModelResponse chat.completion id=chatcmpl-e673ec8e-4e8f-4c9e-bf26-bf9fa7ee52b9 at 0x103a62160> JSON: {
  "object": "chat.completion",
  "choices": [
    {
      "finish_reason": "stop_sequence",
      "index": 0,
      "message": {
        "content": " It's going well, thank you for asking! How about you?",
        "role": "assistant",
        "logprobs": null
      }
    }
  ],
  "id": "chatcmpl-e673ec8e-4e8f-4c9e-bf26-bf9fa7ee52b9",
  "created": 1695222060.917964,
  "model": "claude-instant-1.2",
  "usage": {
    "prompt_tokens": 14,
    "completion_tokens": 9,
    "total_tokens": 23
  }
}, <ModelResponse chat.completion id=chatcmpl-ab6c5bd3-b5d9-4711-9697-e28d9fb8a53c at 0x103a62b60> JSON: {
  "object": "chat.completion",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": " It's going well, thank you for asking! How about you?",
        "role": "assistant",
        "logprobs": null
      }
    }
  ],
  "id": "chatcmpl-ab6c5bd3-b5d9-4711-9697-e28d9fb8a53c",
  "created": 1695222061.0445492,
  "model": "command-nightly",
  "usage": {
    "prompt_tokens": 6,
    "completion_tokens": 14,
    "total_tokens": 20
  }
}, <OpenAIObject chat.completion id=chatcmpl-80szFnKHzCxObW0RqCMw1hWW1Icrq at 0x102dd6430> JSON: {
  "id": "chatcmpl-80szFnKHzCxObW0RqCMw1hWW1Icrq",
  "object": "chat.completion",
  "created": 1695222061,
  "model": "gpt-3.5-turbo-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm an AI language model, so I don't have feelings, but I'm here to assist you with any questions or tasks you might have. How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 39,
    "total_tokens": 52
  }
}]

```
