# Gollem Go 代理框架 (Agent Framework) 搭配 LiteLLM

這是一個展示如何將 [gollem](https://github.com/fugue-labs/gollem)（一個生產級別的 Go 代理框架）與作為 Proxy 閘道器的 LiteLLM 結合使用的範例。這讓 Go 開發者可以透過單一 Proxy 存取 100+ 種 LLM 供應商，同時在工具使用與結構化輸出方面保持編譯時的型別安全。

## 快速入門

### 1. 啟動 LiteLLM Proxy

```bash
# 使用單一模型簡單啟動
litellm --model gpt-4o

# 或使用範例配置進行多供應商存取
litellm --config proxy_config.yaml
```

### 2. 執行範例

```bash
# 安裝 Go 依賴
go mod tidy

# 基礎代理
go run ./basic

# 具備型別安全工具的代理
go run ./tools

# 串流回應
go run ./streaming
```

## 配置

隨附的 `proxy_config.yaml` 透過 LiteLLM 設定了三個供應商：

```yaml
model_list:
  - model_name: gpt-4o          # OpenAI
  - model_name: claude-sonnet    # Anthropic
  - model_name: gemini-pro       # Google Vertex AI
```

在 Go 中只需更改一個字串即可切換供應商 —— 無需更改程式碼：

```go
model := openai.NewLiteLLM("http://localhost:4000",
    openai.WithModel("gpt-4o"),        // OpenAI
    // openai.WithModel("claude-sonnet"),  // Anthropic
    // openai.WithModel("gemini-pro"),     // Google
)
```

## 範例說明

### `basic/` — 基礎代理

將 gollem 連接到 LiteLLM 並執行簡單的提示 (Prompt)。展示了 `NewLiteLLM` 建構函式與基礎代理的建立。

### `tools/` — 型別安全工具

展示了 gollem 的編譯時型別安全工具框架，如何透過 LiteLLM 的工具使用 (Tool-use) 直通功能運作。工具參數是帶有 JSON 標籤的 Go 結構體 —— Schema 會在編譯時自動產生。

### `streaming/` — 串流回應

使用 Go 1.23+ 的 range-over-function 迭代器實現即時 Token 串流，並透過 LiteLLM 的 SSE 直通功能進行代理。

## 運作原理

Gollem 的 `openai.NewLiteLLM()` 建構函式會建立一個指向 LiteLLM Proxy 的 OpenAI 相容供應商。由於 LiteLLM 支援 OpenAI API 協定，因此一切都能開箱即用：

- **對話補全 (Chat completions)** — 標準的請求/回應
- **工具使用 (Tool use)** — LiteLLM 透明地轉發工具定義與呼叫
- **串流 (Streaming)** — 透過 LiteLLM 代理的伺服器發送事件 (SSE)
- **結構化輸出 (Structured output)** — JSON Schema 回應格式可與支援的模型搭配使用

```
Go App (gollem) → LiteLLM Proxy → OpenAI / Anthropic / Google / ...
```

## 為什麼選擇這個？

- **型別安全的 Go**：針對工具、結構化輸出與代理配置進行編譯時型別檢查 —— 避免執行時的意外。
- **單一 Proxy，多種模型**：只需更改模型名稱字串，即可在 OpenAI, Anthropic, Google 及 100+ 其他供應商之間切換。
- **零依賴核心**：gollem 的核心沒有外部依賴 —— 僅使用標準庫 (Stdlib)。
- **單一二進位檔案部署**：`go build` 產生一個二進位檔案，不需要 pip/venv/Docker。
- **成本追蹤與速率限制**：LiteLLM 在 Proxy 層處理成本追蹤、速率限制與回退機制。

## 環境變數

```bash
# 您要使用的供應商所需的金鑰（在 LiteLLM 配置或環境變數中設定）
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# 選用：指向非預設的 LiteLLM Proxy
export LITELLM_PROXY_URL="http://localhost:4000"
```

## 疑難排解

**連線錯誤？**
- 確保 LiteLLM 正在執行：`litellm --model gpt-4o`
- 檢查 URL 是否正確（預設：`http://localhost:4000`）

**找不到模型？**
- 驗證模型名稱是否與 LiteLLM 中配置的相符
- 執行 `curl http://localhost:4000/models` 查看可用模型

**工具呼叫無效？**
- 確保底層模型支援工具使用（GPT-4o, Claude, Gemini）
- 檢查 LiteLLM 日誌以獲取任何供應商特定的錯誤

## 瞭解更多

- [gollem GitHub](https://github.com/fugue-labs/gollem)
- [gollem API 參考](https://pkg.go.dev/github.com/fugue-labs/gollem/core)
- [LiteLLM Proxy 文件](https://docs.litellm.ai/docs/simple_proxy)
- [LiteLLM 支援的模型](https://docs.litellm.ai/docs/providers)
