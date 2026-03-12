# 搭配 LiteLLM Gateway 的 LiveKit Voice Agent

這是一個簡單的範例，展示如何使用 LiveKit 的 xAI realtime plugin 並將 LiteLLM 作為 proxy。這讓您可以在不更改程式碼的情況下，在 xAI、OpenAI 和 Azure realtime APIs 之間切換。

## 快速上手

### 1. 安裝依賴項目

```bash
pip install livekit-agents[xai] websockets
```

### 2. 啟動 LiteLLM proxy

```bash
# 使用 xAI
export XAI_API_KEY="your-xai-key"
litellm --config config.yaml --port 4000
```

### 3. 執行 voice agent

```bash
python main.py
```

輸入您的訊息，即可獲得來自 Grok 的語音回覆！

## Configuration

如果需要，請設定以下環境變數：

```bash
export LITELLM_PROXY_URL="http://localhost:4000"
export LITELLM_API_KEY="sk-1234"
export LITELLM_MODEL="grok-voice-agent"
```

或使用預設值 - 預設連線至 `http://localhost:4000`。

## 範例 Config 檔案

建立一個包含 realtime models 的 `config.yaml`：

```yaml
model_list:
  - model_name: grok-voice-agent
    litellm_params:
      model: xai/grok-2-vision-1212
      api_key: os.environ/XAI_API_KEY
    model_info:
      mode: realtime

  - model_name: openai-voice-agent
    litellm_params:
      model: gpt-4o-realtime-preview
      api_key: os.environ/OPENAI_API_KEY
    model_info:
      mode: realtime

general_settings:
  master_key: sk-1234
```

然後啟動：`litellm --config config.yaml --port 4000`

## 運作原理

LiveKit 的 xAI plugin 透過設定 `base_url` 連接至 LiteLLM proxy：

```python
from livekit.plugins import xai

model = xai.realtime.RealtimeModel(
    voice="ara",
    api_key="sk-1234",              # LiteLLM proxy key
    base_url="http://localhost:4000", # 指向 LiteLLM
)
```

## 切換 Providers

只需在 config 中更改模型即可 - 無需更改程式碼：

**xAI Grok:**
```yaml
model: xai/grok-2-vision-1212
```

**OpenAI:**
```yaml
model: gpt-4o-realtime-preview
```

**Azure OpenAI:**
```yaml
model: azure/gpt-4o-realtime-preview
api_base: https://your-endpoint.openai.azure.com/
```

## 為什麼要使用 LiteLLM？

- ✅ **切換 providers** 無需更改 agent 程式碼
- ✅ **Cost tracking** 涵蓋所有 voice sessions
- ✅ **Rate limiting** 與預算管理
- ✅ **Load balancing** 橫跨多個 API keys
- ✅ **Fallbacks** 至備用模型

## 了解更多

- [LiveKit xAI Realtime Tutorial](/docs/tutorials/livekit_xai_realtime)
- [xAI Realtime Docs](/docs/providers/xai_realtime)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)
- [LiteLLM Realtime API](/docs/realtime)
