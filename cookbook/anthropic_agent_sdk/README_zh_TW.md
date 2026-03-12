# Claude Agent SDK 搭配 LiteLLM 閘道器

一個簡單的範例，展示如何將 Claude 的 Agent SDK 與作為代理伺服器的 LiteLLM 結合使用。這讓您可以透過 Agent SDK 使用任何 LLM 供應商（OpenAI、Bedrock、Azure 等）。

## 快速上手

### 1. 安裝依賴項目

```bash
pip install anthropic claude-agent-sdk litellm
```

### 2. 啟動 LiteLLM 代理伺服器

```bash
# 使用 Claude 簡單啟動
litellm --model claude-sonnet-4-20250514

# 或使用設定檔啟動
litellm --config config.yaml
```

### 3. 執行對話

**基本代理 (無 MCP)：**

```bash
python main.py
```

**帶有 MCP 的代理 (使用 DeepWiki2 進行研究)：**

```bash
python agent_with_mcp.py
```

如果 MCP 連線失敗，您可以禁用它：

```bash
USE_MCP=false python agent_with_mcp.py
```

就這樣！您現在可以在終端機中與代理進行對話了。

### 對話命令

在對話時，您可以使用以下命令：
- `models` - 列出所有可用模型（從您的 LiteLLM 代理伺服器獲取）
- `model` - 切換到不同的模型
- `clear` - 開始新的對話
- `quit` 或 `exit` - 結束對話

對話會自動從您 LiteLLM 代理伺服器的 `/models` 端點獲取可用模型，因此您始終可以看到目前設定的模型。

## 設定

如有需要，請設定這些環境變數：

```bash
export LITELLM_PROXY_URL="http://localhost:4000"
export LITELLM_API_KEY="sk-1234"
export LITELLM_MODEL="bedrock-claude-sonnet-4.5"
```

或者直接使用預設值 - 它預設會連接到 `http://localhost:4000`。

## 檔案說明

- `main.py` - 不含 MCP 的基本互動式代理
- `agent_with_mcp.py` - 包含 MCP 伺服器整合 (DeepWiki2) 的代理
- `common.py` - 共用的實用程式和函數
- `config.example.yaml` - LiteLLM 設定範例
- `requirements.txt` - Python 依賴項目

## 設定檔範例

如果您想使用多個模型，請建立 `config.yaml`（參考 `config.example.yaml`）：

```yaml
model_list:
  - model_name: bedrock-claude-sonnet-4
    litellm_params:
      model: "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0"
      aws_region_name: "us-east-1"

  - model_name: bedrock-claude-sonnet-4.5
    litellm_params:
      model: "bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0"
      aws_region_name: "us-east-1"
```

然後使用以下命令啟動 LiteLLM：`litellm --config config.yaml`

## 運作原理

關鍵在於將 Agent SDK 指向 LiteLLM 而非直接指向 Anthropic：

```python
# 指向 LiteLLM 閘道器 (而非 Anthropic)
os.environ["ANTHROPIC_BASE_URL"] = "http://localhost:4000"
os.environ["ANTHROPIC_API_KEY"] = "sk-1234"  # 您的 LiteLLM 金鑰

# 使用 LiteLLM 中設定的任何模型
options = ClaudeAgentOptions(
    model="bedrock-claude-sonnet-4",  # 或 gpt-4，或任何其他模型
    system_prompt="您是一位得力的助手。",
    max_turns=50,
)
```

注意：不要在基礎 URL 中添加 `/anthropic` - LiteLLM 會自動處理路由。

## 為什麼要使用這個？

- **輕鬆切換供應商**：在 OpenAI、Bedrock、Azure 等之間使用相同的程式碼。
- **成本追蹤**：LiteLLM 會追蹤您所有代理對話的支出。
- **速率限制**：為您的代理使用設定預算和限制。
- **負載平衡**：在多個 API 金鑰或區域之間分配請求。
- **備援機制 (Fallbacks)**：如果一個模型失敗，自動嘗試使用另一個模型。

## 疑難排解

**連線錯誤？**
- 確保 LiteLLM 正在執行：`litellm --model your-model`
- 檢查 URL 是否正確（預設：`http://localhost:4000`）

**驗證錯誤？**
- 驗證您的 LiteLLM API 金鑰是否正確
- 確保模型已在您的 LiteLLM 設定中配置

**找不到模型？**
- 檢查模型名稱是否與您 LiteLLM 設定中的名稱相符
- 執行 `litellm --model your-model` 來測試它是否正常工作

**帶有 MCP 的代理卡住或失敗？**
- MCP 伺服器可能在 `http://localhost:4000/mcp/deepwiki2` 無法使用
- 嘗試禁用 MCP：`USE_MCP=false python agent_with_mcp.py`
- 或使用基本代理：`python main.py`

## 了解更多

- [LiteLLM 文件](https://docs.litellm.ai/)
- [Claude Agent SDK](https://github.com/anthropics/anthropic-agent-sdk)
- [LiteLLM 代理伺服器指南](https://docs.litellm.ai/docs/proxy/quick_start)
