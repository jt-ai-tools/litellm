import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 使用 PDF 輸入 (Using PDF Input)

如何發送 / 接收 PDF（或其他文件類型）到 `/chat/completions` 端點

適用於：
- Vertex AI 模型 (Gemini + Anthropic)
- Bedrock 模型
- Anthropic API 模型
- OpenAI API 模型
- Mistral (僅使用已上傳文件的檔案 ID，類似於 OpenAI 的 file_id 輸入)

## 快速上手 (Quick Start)

### URL 

<Tabs>
<TabItem value="sdk" label="SDK">

```python
from litellm.utils import supports_pdf_input, completion

# 設置 AWS 憑證
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION_NAME"] = ""


# pdf url
file_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# model
model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"

file_content = [
    {"type": "text", "text": "What's this file about?"},
    {
        "type": "file",
        "file": {
            "file_id": file_url,
        }
    },
]


if not supports_pdf_input(model, None):
    print("Model does not support image input")

response = completion(
    model=model,
    messages=[{"role": "user", "content": file_content}],
)
assert response is not None
```
</TabItem>
<TabItem value="proxy" label="PROXY">

1. 設置 config.yaml

```yaml
model_list:
  - model_name: bedrock-model
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: os.environ/AWS_REGION_NAME
```

2. 啟動代理伺服器 (proxy)

```bash
litellm --config /path/to/config.yaml
```

3. 測試它！ 

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
    "model": "bedrock-model",
    "messages": [
        {"role": "user", "content": [
            {"type": "text", "text": "What's this file about?"},
            {
                "type": "file",
                "file": {
                    "file_id": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                }
            }
        ]},
    ]
}'
```
</TabItem>
</Tabs>

### base64

<Tabs>
<TabItem value="sdk" label="SDK">

```python
from litellm.utils import supports_pdf_input, completion

# 設置 AWS 憑證
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION_NAME"] = ""


# pdf url
image_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
response = requests.get(url)
file_data = response.content

encoded_file = base64.b64encode(file_data).decode("utf-8")
base64_url = f"data:application/pdf;base64,{encoded_file}"

# model
model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"

file_content = [
    {"type": "text", "text": "What's this file about?"},
    {
        "type": "file",
        "file": {
            "file_data": base64_url,
        }
    },
]


if not supports_pdf_input(model, None):
    print("Model does not support image input")

response = completion(
    model=model,
    messages=[{"role": "user", "content": file_content}],
)
assert response is not None
```
</TabItem>
<TabItem value="proxy" label="PROXY">

1. 設置 config.yaml

```yaml
model_list:
  - model_name: bedrock-model
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: os.environ/AWS_REGION_NAME
```

2. 啟動代理伺服器 (proxy)

```bash
litellm --config /path/to/config.yaml
```

3. 測試它！ 

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
    "model": "bedrock-model",
    "messages": [
        {"role": "user", "content": [
            {"type": "text", "text": "What's this file about?"},
            {
                "type": "file",
                "file": {
                    "file_data": "data:application/pdf;base64...",
                }
            }
        ]},
    ]
}'
```
</TabItem>
</Tabs>

## 指定格式 (Specifying format)

要指定文件的格式，您可以使用 `format` 參數。 


<Tabs>
<TabItem value="sdk" label="SDK">

```python
from litellm.utils import supports_pdf_input, completion

# 設置 AWS 憑證
os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION_NAME"] = ""


# pdf url
file_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# model
model = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"

file_content = [
    {"type": "text", "text": "What's this file about?"},
    {
        "type": "file",
        "file": {
            "file_id": file_url,
            "format": "application/pdf",
        }
    },
]


if not supports_pdf_input(model, None):
    print("Model does not support image input")

response = completion(
    model=model,
    messages=[{"role": "user", "content": file_content}],
)
assert response is not None
```
</TabItem>
<TabItem value="proxy" label="PROXY">

1. 設置 config.yaml

```yaml
model_list:
  - model_name: bedrock-model
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: os.environ/AWS_REGION_NAME
```

2. 啟動代理伺服器 (proxy)

```bash
litellm --config /path/to/config.yaml
```

3. 測試它！ 

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
    "model": "bedrock-model",
    "messages": [
        {"role": "user", "content": [
            {"type": "text", "text": "What's this file about?"},
            {
                "type": "file",
                "file": {
                    "file_id": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "format": "application/pdf",
                }
            }
        ]},
    ]
}'
```
</TabItem>
</Tabs>


## Mistral 範例 (Mistral Example)

以下是使用 Mistral 模型進行文件理解的樣本有效負載 (payload)：


<Tabs>
<TabItem value="sdk" label="SDK">

```python
from litellm.utils import completion

# 從 files 端點接收到的 pdf file_id
file_id = "fa778e5e-46ec-4562-8418-36623fe25a71"

# model
model = "mistral/mistral-large-latest"

file_content = [
    {"type": "text", "text": "What's this file about?"},
    {
        "type": "file",
        "file": {
            "file_id": file_id,
        }
    },
]

response = completion(
    model=model,
    messages=[{"role": "user", "content": file_content}],
)
assert response is not None
```

</TabItem>
<TabItem value="proxy" label="PROXY">

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
    "model": "mistral/mistral-large-latest",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is the content of the file?"
                },
                {
                    "type": "file",
                    "file": {
                        "file_id": "fa778e5e-46ec-4562-8418-36623fe25a71"
                    }
                }
            ]
        }
    ]
}
```
</TabItem>
</Tabs>

## 檢查模型是否支援 PDF 輸入

<Tabs>
<TabItem label="SDK" value="sdk">

使用 `litellm.supports_pdf_input(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0")` -> 如果模型可以接收 PDF 輸入則返回 `True`

```python
assert litellm.supports_pdf_input(model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0") == True
```
</TabItem>

<TabItem label="PROXY" value="proxy">

1. 在 config.yaml 中定義 Bedrock 模型

```yaml
model_list:
  - model_name: bedrock-model # 模型群組名稱
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: os.environ/AWS_REGION_NAME
    model_info: # 選填 - 手動設置
      supports_pdf_input: True
```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 呼叫 `/model_group/info` 檢查模型是否支援 `pdf` 輸入

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
      "model_group": "bedrock-model",
      "providers": ["bedrock"],
      "max_input_tokens": 128000,
      "max_output_tokens": 16384,
      "mode": "chat",
      ...,
      "supports_pdf_input": true, # 👈 supports_pdf_input 為 true
    }
  ]
}
```

</TabItem>
</Tabs>
