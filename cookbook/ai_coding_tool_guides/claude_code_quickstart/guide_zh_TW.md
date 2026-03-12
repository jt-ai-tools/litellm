# Claude Code 搭配 LiteLLM 快速上手指南

本指南展示如何透過 LiteLLM 代理程式從 Claude Code 呼叫 Claude 模型（以及任何 LiteLLM 支援的模型）。

> **注意：** 此整合基於 [Anthropic 官方 LiteLLM 設定文件](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#litellm-configuration)。它允許您透過 Claude Code 使用任何 LiteLLM 支援的模型，並實現集中式身分驗證、用量追蹤和成本控制。

## 影片示範

觀看完整教學：https://www.loom.com/embed/3c17d683cdb74d36a3698763cc558f56

## 先決條件

- 已安裝 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
- 您所選供應商的 API 金鑰

## 安裝

首先，安裝支援代理伺服器的 LiteLLM：

```bash
pip install 'litellm[proxy]'
```

## 步驟 1：設定 config.yaml

使用環境變數建立安全的設定檔：

```yaml
model_list:
  # Claude 模型
  - model_name: claude-3-5-sonnet-20241022    
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
  
  - model_name: claude-3-5-haiku-20241022
    litellm_params:
      model: anthropic/claude-3-5-haiku-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  
litellm_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

設定您的環境變數：

```bash
export ANTHROPIC_API_KEY="您的-anthropic-api-key"
export LITELLM_MASTER_KEY="sk-1234567890"  # 生成一個安全的金鑰
```

## 步驟 2：啟動代理伺服器 (Proxy)

```bash
litellm --config /path/to/config.yaml

# 運行於 http://0.0.0.0:4000
```

## 步驟 3：驗證設定

測試您的代理伺服器是否正常運作：

```bash
curl -X POST http://0.0.0.0:4000/v1/messages \
-H "Authorization: Bearer $LITELLM_MASTER_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "法國的首都是哪裡？"}]
}'
```

## 步驟 4：設定 Claude Code

### 方法 1：統一端點 (推薦)

設定 Claude Code 使用 LiteLLM 的統一端點。這裡可以使用虛擬金鑰 (virtual key) 或主金鑰 (master key)：

```bash
export ANTHROPIC_BASE_URL="http://0.0.0.0:4000"
export ANTHROPIC_AUTH_TOKEN="$LITELLM_MASTER_KEY"
```

> **提示：** LITELLM_MASTER_KEY 讓 Claude 可以存取所有代理模型，而虛擬金鑰則會被限制在 UI 中設定的模型。

### 方法 2：供應商特定的直通 (Pass-through) 端點

或者，使用 Anthropic 直通端點：

```bash
export ANTHROPIC_BASE_URL="http://0.0.0.0:4000/anthropic"
export ANTHROPIC_AUTH_TOKEN="$LITELLM_MASTER_KEY"
```

## 步驟 5：使用 Claude Code

### 選擇您的模型

您有兩種方式可以指定 Claude Code 使用的模型：

#### 選項 1：命令列 / 工作階段模型選擇

在啟動 Claude Code 時或在工作階段中直接指定模型：

```bash
# 啟動時指定模型
claude --model claude-3-5-sonnet-20241022

# 或在工作階段中更改模型
/model claude-3-5-haiku-20241022
```

此方法會使用您確切指定的模型。

#### 選項 2：環境變數

使用環境變數設定預設模型：

```bash
# 告訴 Claude Code 預設使用哪些模型
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-3-5-sonnet-20241022
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-3-5-haiku-20241022
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-3-5-20240229

claude  # 將使用上述指定的模型
```

**注意：** Claude Code 可能會快取先前工作階段的模型。如果環境變數沒有生效，請使用選項 1 明確設定模型。

**重要：** 您 LiteLLM 設定中的 `model_name` 必須與 Claude Code 請求的模型名稱（來自環境變數或命令列）相符。

### 使用 1M 上下文視窗

Claude Code 支援 Claude 4+ 模型使用擴展上下文（100 萬個權杖），只需加上 `[1m]` 後綴：

```bash
# 使用 Sonnet 4.5 並開啟 1M 上下文（Shell 中需要引號）
claude --model 'claude-sonnet-4-5-20250929[1m]'

# 在 Claude Code 工作階段內（不需要引號）
/model claude-sonnet-4-5-20250929[1m]
```

**重要：** 在 Shell 中將 `--model` 與 `[1m]` 一起使用時，必須使用引號以防止 Shell 解析方括號。

或者，透過環境變數設定為預設值：

```bash
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5-20250929[1m]'
claude
```

**運作原理：**
- Claude Code 在發送到 LiteLLM 之前會移除 `[1m]` 後綴
- Claude Code 會自動添加標頭 `anthropic-beta: context-1m-2025-08-07`
- 您的 LiteLLM 設定 **不應** 在模型名稱中包含 `[1m]`

**驗證 1M 上下文是否啟用：**
```bash
/context
# 應該顯示：21k/1000k tokens (2%)
```

**定價：** 使用 1M 上下文的模型有不同的計費方式。超過 20 萬個輸入權杖的部分將以較高的費率計費。

## 疑難排解

常見問題與解決方案：

**Claude Code 無法連線：**
- 驗證您的代理伺服器是否正在運行：`curl http://0.0.0.0:4000/health`
- 檢查 `ANTHROPIC_BASE_URL` 是否設定正確
- 確保您的 `ANTHROPIC_AUTH_TOKEN` 與您的 LiteLLM 主金鑰相符

**驗證錯誤：**
- 驗證您的環境變數已設定：`echo $LITELLM_MASTER_KEY`
- 檢查您的 API 金鑰是否有效且餘額充足
- 確保 `ANTHROPIC_AUTH_TOKEN` 與您的 LiteLLM 主金鑰相符

**找不到模型：**
- 在 LiteLLM 日誌中查看 Claude Code 請求的是哪個模型
- 確保您的 `config.yaml` 中有相符的 `model_name` 條目
- 如果使用環境變數，請驗證它們已設定：`echo $ANTHROPIC_DEFAULT_SONNET_MODEL`

**1M 上下文未運作（顯示 200k 而非 1000k）：**
- 驗證您是否使用了 `[1m]` 後綴：`/model your-model-name[1m]`
- 檢查 LiteLLM 日誌中請求頭是否包含 `context-1m-2025-08-07`
- 確保您的模型支援 1M 上下文（僅限特定的 Claude 模型）
- 您的 LiteLLM 設定 **不應** 在 `model_name` 中包含 `[1m]`

## 使用多個模型和供應商

您可以設定 LiteLLM 路由到任何支援的供應商。以下是多供應商的範例：

```yaml
model_list:
  # OpenAI 模型
  - model_name: codex-mini
    litellm_params:
      model: openai/codex-mini
      api_key: os.environ/OPENAI_API_KEY
      api_base: https://api.openai.com/v1

  - model_name: o3-pro
    litellm_params:
      model: openai/o3-pro
      api_key: os.environ/OPENAI_API_KEY
      api_base: https://api.openai.com/v1

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      api_base: https://api.openai.com/v1

  # Anthropic 模型
  - model_name: claude-3-5-sonnet-20241022
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-3-5-haiku-20241022
    litellm_params:
      model: anthropic/claude-3-5-haiku-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

  # AWS Bedrock
  - model_name: claude-bedrock
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0
      aws_access_key_id: os.environ/AWS_ACCESS_KEY_ID
      aws_secret_access_key: os.environ/AWS_SECRET_ACCESS_KEY
      aws_region_name: us-east-1

litellm_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

**注意：** `model_name` 可以是您選擇的任何名稱。Claude Code 會請求您指定的任何模型（透過環境變數或命令列），而 LiteLLM 會路由到 `litellm_params` 中設定的 `model`。

無縫切換模型：

```bash
# 使用環境變數設定預設值
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-3-5-sonnet-20241022
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-3-5-haiku-20241022

# 或直接指定
claude --model claude-3-5-sonnet-20241022  # 複雜推理
claude --model claude-3-5-haiku-20241022    # 快速回應
claude --model claude-bedrock                # Bedrock 部署
```

## Claude Code 使用的預設模型

如果您 **沒有** 設定環境變數，Claude Code 會使用以下預設模型名稱：

| 用途 | 預設模型名稱 (v2.1.14) |
|---------|------------------------------|
| 主要模型 | `claude-sonnet-4-5-20250929` |
| 輕量任務 (子代理、摘要) | `claude-haiku-4-5-20251001` |
| 規劃模式 | `claude-opus-4-5-20251101` |

如果您希望 Claude Code 在不設定環境變數的情況下運作，您的 LiteLLM 設定應包含這些模型名稱：

```yaml
model_list:
  - model_name: claude-sonnet-4-5-20250929
    litellm_params:
      # 可以是任何供應商 - Anthropic、Bedrock、Vertex AI 等。
      model: anthropic/claude-sonnet-4-5-20250929
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-haiku-4-5-20251001
    litellm_params:
      model: anthropic/claude-haiku-4-5-20251001
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: claude-opus-4-5-20251101
    litellm_params:
      model: anthropic/claude-opus-4-5-20251101
      api_key: os.environ/ANTHROPIC_API_KEY
```

**警告：** 這些預設模型名稱可能會隨新版本的 Claude Code 而改變。請檢查 LiteLLM 代理日誌中的 "model not found" 錯誤，以識別 Claude Code 請求的是什麼。

## 額外資源

- [LiteLLM 文件](https://docs.litellm.ai/)
- [Claude Code 文件](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Anthropic 的 LiteLLM 設定指南](https://docs.anthropic.com/en/docs/claude-code/llm-gateway#litellm-configuration)
