import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 使用音訊模型 (Audio Models)

如何發送 / 接收音訊到 `/chat/completions` 端點


## 來自模型的音訊輸出 (Audio Output)

為提示詞建立類人音訊回應的範例

<Tabs>

<TabItem label="LiteLLM Python SDK" value="Python">

```python
import os 
import base64
from litellm import completion

os.environ["OPENAI_API_KEY"] = "your-api-key"

# openai call
completion = await litellm.acompletion(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[{"role": "user", "content": "Is a golden retriever a good family dog?"}],
)

wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("dog.wav", "wb") as f:
    f.write(wav_bytes)
```

</TabItem>
<TabItem label="LiteLLM Proxy Server" value="proxy">

1. 在 config.yaml 中定義音訊模型

```yaml
model_list:
  - model_name: gpt-4o-audio-preview # OpenAI gpt-4o-audio-preview
    litellm_params:
      model: openai/gpt-4o-audio-preview
      api_key: os.environ/OPENAI_API_KEY 

```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 使用 OpenAI Python SDK 進行測試


```python
import base64
from openai import OpenAI

client = OpenAI(
    api_key="LITELLM_PROXY_KEY", # sk-1234
    base_url="LITELLM_PROXY_BASE" # http://0.0.0.0:4000
)

completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": "Is a golden retriever a good family dog?"
        }
    ]
)

print(completion.choices[0])

wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("dog.wav", "wb") as f:
    f.write(wav_bytes)

```




</TabItem>
</Tabs>

## 輸入音訊到模型 (Audio Input)


<Tabs>

<TabItem label="LiteLLM Python SDK" value="Python">

```python
import base64
import requests

url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()
wav_data = response.content
encoded_string = base64.b64encode(wav_data).decode("utf-8")

completion = litellm.completion(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this recording?"},
                {
                    "type": "input_audio",
                    "input_audio": {"data": encoded_string, "format": "wav"},
                },
            ],
        },
    ],
)

print(completion.choices[0].message)
```

</TabItem>

<TabItem label="LiteLLM Proxy Server" value="proxy">


1. 在 config.yaml 中定義音訊模型

```yaml
model_list:
  - model_name: gpt-4o-audio-preview # OpenAI gpt-4o-audio-preview
    litellm_params:
      model: openai/gpt-4o-audio-preview
      api_key: os.environ/OPENAI_API_KEY 

```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 使用 OpenAI Python SDK 進行測試


```python
import base64
from openai import OpenAI

client = OpenAI(
    api_key="LITELLM_PROXY_KEY", # sk-1234
    base_url="LITELLM_PROXY_BASE" # http://0.0.0.0:4000
)


# 獲取音訊檔案並將其轉換為 base64 編碼字串
url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()
wav_data = response.content
encoded_string = base64.b64encode(wav_data).decode('utf-8')

completion = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {
            "role": "user",
            "content": [
                { 
                    "type": "text",
                    "text": "What is in this recording?"
                },
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_string,
                        "format": "wav"
                    }
                }
            ]
        },
    ]
)

print(completion.choices[0].message)
```


</TabItem>
</Tabs>

## 檢查模型是否支援 `audio_input` 和 `audio_output`

<Tabs>
<TabItem label="LiteLLM Python SDK" value="Python">

使用 `litellm.supports_audio_output(model="")` -> 如果模型可以產生音訊輸出則返回 `True`

使用 `litellm.supports_audio_input(model="")` -> 如果模型可以接收音訊輸入則返回 `True`

```python
assert litellm.supports_audio_output(model="gpt-4o-audio-preview") == True
assert litellm.supports_audio_input(model="gpt-4o-audio-preview") == True

assert litellm.supports_audio_output(model="gpt-3.5-turbo") == False
assert litellm.supports_audio_input(model="gpt-3.5-turbo") == False
```
</TabItem>

<TabItem label="LiteLLM Proxy Server" value="proxy">


1. 在 config.yaml 中定義願景模型 (vision models)

```yaml
model_list:
  - model_name: gpt-4o-audio-preview # OpenAI gpt-4o-audio-preview
    litellm_params:
      model: openai/gpt-4o-audio-preview
      api_key: os.environ/OPENAI_API_KEY
  - model_name: llava-hf          # 自定義 OpenAI 相容模型
    litellm_params:
      model: openai/llava-hf/llava-v1.6-vicuna-7b-hf
      api_base: http://localhost:8000
      api_key: fake-key
    model_info:
      supports_audio_output: True        # 將 supports_audio_output 設置為 True，以便 /model/info 返回此屬性為 True
      supports_audio_input: True         # 將 supports_audio_input 設置為 True，以便 /model/info 返回此屬性為 True
```

2. 執行代理伺服器 (proxy server)

```bash
litellm --config config.yaml
```

3. 呼叫 `/model_group/info` 檢查您的模型是否支援 `vision`

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
      "model_group": "gpt-4o-audio-preview",
      "providers": ["openai"],
      "max_input_tokens": 128000,
      "max_output_tokens": 16384,
      "mode": "chat",
      "supports_audio_output": true, # 👈 supports_audio_output 為 true
      "supports_audio_input": true, # 👈 supports_audio_input 為 true
    },
    {
      "model_group": "llava-hf",
      "providers": ["openai"],
      "max_input_tokens": null,
      "max_output_tokens": null,
      "mode": null,
      "supports_audio_output": true, # 👈 supports_audio_output 為 true
      "supports_audio_input": true, # 👈 supports_audio_input 為 true
    }
  ]
}
```

</TabItem>
</Tabs>


## 包含音訊的回應格式 (Response Format with Audio)

以下是當向模型發送音訊輸入時，您可能從 `/chat/completions` 端點接收到的 `message` JSON 資料結構範例。

```json
{
  "index": 0,
  "message": {
    "role": "assistant",
    "content": null,
    "refusal": null,
    "audio": {
      "id": "audio_abc123",
      "expires_at": 1729018505,
      "data": "<bytes omitted>",
      "transcript": "Yes, golden retrievers are known to be ..."
    }
  },
  "finish_reason": "stop"
}
```
- `audio` 如果請求了音訊輸出模態 (modality)，此對象包含有關模型音訊回應的數據
    - `audio.id` 音訊回應的唯一識別碼
    - `audio.expires_at` 此音訊回應在伺服器上不再可供多輪對話使用的 Unix 時間戳（秒）。
    - `audio.data` 模型產生的 Base64 編碼音訊位元組，格式在請求中指定。
    - `audio.transcript` 模型產生的音訊逐字稿 (Transcript)。
