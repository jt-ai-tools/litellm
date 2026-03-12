import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 電腦使用 (Computer Use)

電腦使用允許模型藉由擷取螢幕截圖並執行點擊、輸入和捲動等操作來與電腦介面互動。這使得 AI 模型能夠自主操作桌面環境。

**支援的供應商：**
- Anthropic API (`anthropic/`)
- Bedrock (Anthropic) (`bedrock/`)
- Vertex AI (Anthropic) (`vertex_ai/`)

**支援的工具類型：**
- `computer` - 具有顯示參數的電腦互動工具
- `bash` - Bash shell 工具  
- `text_editor` - 文字編輯器工具
- `web_search` - 網頁搜尋工具

LiteLLM 將在所有支援的供應商中標準化電腦使用工具。

## 快速上手 (Quick Start)

<Tabs>
<TabItem value="sdk" label="LiteLLM Python SDK">

```python
import os 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

# 電腦使用工具
    tools = [
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_height_px": 768,
            "display_width_px": 1024,
            "display_number": 0,
        }
    ]
    
    messages = [
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                "text": "Take a screenshot and tell me what you see"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                }
            }
        ]
    }
]

response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
    messages=messages,
    tools=tools,
)

print(response)
```

</TabItem>
<TabItem value="proxy" label="LiteLLM Proxy Server">

1. 在 config.yaml 中定義電腦使用模型

```yaml
model_list:
  - model_name: claude-3-5-sonnet-latest # Anthropic claude-3-5-sonnet-latest
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: claude-bedrock         # Bedrock Anthropic 模型
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-west-2
    model_info:
      supports_computer_use: True        # 將 supports_computer_use 設置為 True，以便 /model/info 返回此屬性為 True
```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 使用 OpenAI Python SDK 進行測試

```python
import os 
from openai import OpenAI

client = OpenAI(
    api_key="sk-1234", # 您的 litellm proxy api key
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="claude-3-5-sonnet-latest",
    messages=[
        {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": "Take a screenshot and tell me what you see"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    }
                }
            ]
        }
    ],
    tools=[
        {
            "type": "computer_20241022",
            "name": "computer",
            "display_height_px": 768,
            "display_width_px": 1024,
            "display_number": 0,
        }
    ]
)

print(response)
```

</TabItem>
</Tabs>

## 檢查模型是否支援 `computer use`

<Tabs>
<TabItem label="LiteLLM Python SDK" value="Python">

使用 `litellm.supports_computer_use(model="")` -> 如果模型支援電腦使用則返回 `True`，否則返回 `False`

```python
import litellm

assert litellm.supports_computer_use(model="anthropic/claude-3-5-sonnet-latest") == True
assert litellm.supports_computer_use(model="anthropic/claude-3-7-sonnet-20250219") == True
assert litellm.supports_computer_use(model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0") == True
assert litellm.supports_computer_use(model="vertex_ai/claude-3-5-sonnet") == True
assert litellm.supports_computer_use(model="openai/gpt-4") == False
```
</TabItem>

<TabItem label="LiteLLM Proxy Server" value="proxy">

1. 在 config.yaml 中定義電腦使用模型

```yaml
model_list:
  - model_name: claude-3-5-sonnet-latest # Anthropic claude-3-5-sonnet-latest
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: claude-bedrock         # Bedrock Anthropic 模型
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-west-2
    model_info:
      supports_computer_use: True        # 將 supports_computer_use 設置為 True，以便 /model/info 返回此屬性為 True
```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 呼叫 `/model_group/info` 檢查您的模型是否支援 `computer use`

```shell
curl -X 'GET' \
  'http://localhost:4000/model_group/info' \
  -H 'accept: application/json' \
  -H 'x-api-key: sk-1234'
```

預期回應 (Expected Response)

```json
{
  "data": [
    {
      "model_group": "claude-3-5-sonnet-latest",
      "providers": ["anthropic"],
      "max_input_tokens": 200000,
      "max_output_tokens": 8192,
      "mode": "chat",
      "supports_computer_use": true, # 👈 supports_computer_use 為 true
      "supports_vision": true,
      "supports_function_calling": true
    },
    {
      "model_group": "claude-bedrock",
      "providers": ["bedrock"],
      "max_input_tokens": 200000,
      "max_output_tokens": 8192,
      "mode": "chat",
      "supports_computer_use": true, # 👈 supports_computer_use 為 true
      "supports_vision": true,
      "supports_function_calling": true
    }
  ]
}
```

</TabItem>
</Tabs>

## 不同的工具類型 (Different Tool Types)

電腦使用支援多種不同的工具類型，用於各種互動模式：

<Tabs>
<TabItem value="computer" label="Computer Tool">

`computer_20241022` 工具提供直接的螢幕互動能力。

```python
import os 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

tools = [
    {
        "type": "computer_20241022", 
        "name": "computer",
        "display_height_px": 768,
        "display_width_px": 1024,
        "display_number": 0,
    }
]

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": "Click on the search button in the screenshot"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                }
            }
        ]
    }
]

response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
    messages=messages,
    tools=tools,
)

print(response)
```

</TabItem>
<TabItem value="bash" label="Bash Tool">

`bash_20241022` 工具提供命令列介面 (CLI) 存取。

```python
import os 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

tools = [
    {
        "type": "bash_20241022",
        "name": "bash"
    }
]

messages = [
    {
        "role": "user",
        "content": "List the files in the current directory using bash"
    }
]

response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
    messages=messages,
    tools=tools,
)

print(response)
```

</TabItem>
<TabItem value="text_editor" label="Text Editor Tool">

`text_editor_20250124` 工具提供文字檔案編輯能力。

```python
import os 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

tools = [
    {
        "type": "text_editor_20250124",
        "name": "str_replace_editor"
    }
]

messages = [
    {
        "role": "user",
        "content": "Create a simple Python hello world script"
    }
]

response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
    messages=messages,
    tools=tools,
)

print(response)
```

</TabItem>
</Tabs>

## 使用多個工具的高級用法 (Advanced Usage with Multiple Tools)

您可以在單個請求中結合不同的電腦使用工具：

```python
import os 
from litellm import completion

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

tools = [
    {
        "type": "computer_20241022",
        "name": "computer", 
        "display_height_px": 768,
        "display_width_px": 1024,
        "display_number": 0,
    },
    {
        "type": "bash_20241022",
        "name": "bash"
    },
    {
        "type": "text_editor_20250124", 
        "name": "str_replace_editor"
    }
]

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Take a screenshot, then create a file describing what you see, and finally use bash to show the file contents"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    }
                }
            ]
        }
    ]
    
response = completion(
    model="anthropic/claude-3-5-sonnet-latest",
            messages=messages,
            tools=tools,
)

print(response)
```

## 規範 (Spec)

### 電腦工具 (Computer Tool - `computer_20241022`)

```json
{
  "type": "computer_20241022",
  "name": "computer",
  "display_height_px": 768,    // 必填：螢幕高度（像素）
  "display_width_px": 1024,    // 必填：螢幕寬度（像素）
  "display_number": 0          // 選填：顯示器編號（預設：0）
}
```

### Bash 工具 (Bash Tool - `bash_20241022`)

```json
{
  "type": "bash_20241022", 
  "name": "bash"              // 必填：工具名稱
}
```

### 文字編輯器工具 (Text Editor Tool - `text_editor_20250124`)

```json
{
  "type": "text_editor_20250124",
  "name": "str_replace_editor"  // 必填：工具名稱
}
```

### 網頁搜尋工具 (Web Search Tool - `web_search_20250305`)

```json
{
  "type": "web_search_20250305",
  "name": "web_search"         // 必填：工具名稱
}
```
