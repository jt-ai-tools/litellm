# LITELM 指令指南

本文件為在 LiteLLM 倉庫中工作的 AI 代理提供全面的操作指令。

## 總覽

LiteLLM 是一個統一的 100+ 種 LLM 介面，具備以下功能：
- 將輸入翻譯為各供應商特定的補全 (Completion)、嵌入 (Embedding) 和圖像生成端點。
- 為所有供應商提供一致的 OpenAI 格式輸出。
- 包含跨多個部署的重試/回退邏輯 (Router)。
- 提供具備預算、速率限制和身份驗證功能的代理伺服器 (AI 閘道器)。
- 支援進階功能，如工具呼叫 (Function Calling)、串流 (Streaming)、快取 (Caching) 和可觀測性 (Observability)。

## 倉庫結構

### 核心組件
- `litellm/` - 主要函式庫程式碼
  - `llms/` - 各供應商特定的實作（OpenAI, Anthropic, Azure 等）
  - `proxy/` - 代理伺服器實作 (AI 閘道器)
  - `router_utils/` - 負載平衡與回退邏輯
  - `types/` - 型別定義與 Schema
  - `integrations/` - 第三方整合（可觀測性、快取等）

### 關鍵目錄
- `tests/` - 全面的測試套件
- `docs/my-website/` - 文件網站
- `ui/litellm-dashboard/` - 管理員儀表板 UI
- `enterprise/` - 企業版專屬功能

## 開發指南

### 修改程式碼

1. **供應商實作**：當新增/修改 LLM 供應商時：
   - 遵循 `litellm/llms/{provider}/` 中的現有模式。
   - 實作繼承自 `BaseConfig` 的正確轉換類別。
   - 同時支援同步和非同步操作。
   - 適當處理串流回應。
   - 包含具備供應商特定異常的正確錯誤處理。

2. **型別安全**：
   - 全程使用正確的型別提示 (Type Hints)。
   - 更新 `litellm/types/` 中的型別定義。
   - 確保與 Pydantic v1 和 v2 的相容性。

3. **測試**：
   - 在適當的 `tests/` 子目錄中加入測試。
   - 包含單元測試與整合測試。
   - 徹底測試供應商特定的功能。
   - 考慮為效能關鍵的變更加入負載測試。

### 修改 UI 程式碼（後端開發請忽略）

1. **Tremor 已棄用，請勿在新的功能/變更中使用 Tremor 組件**
   - 唯一的例外是 Tremor Table 組件及其必要的子組件。

2. **盡可能使用通用組件 (Common Components)**：
   - 這些組件通常定義在 `common_components` 目錄中。
   - 應優先使用這些組件，避免除非必要否則不建立新組件。

3. **測試**：
   - 程式碼庫使用 **Vitest** 和 **React Testing Library**。
   - **查詢優先級順序 (Query Priority Order)**：依序使用以下查詢方法：`getByRole`, `getByLabelText`, `getByPlaceholderText`, `getByText`, `getByTestId`。
   - **始終使用 `screen`**，而非從 `render()` 解構（例如：使用 `screen.getByText()` 而非 `getByText()`）。
   - **將使用者互動包裝在 `act()` 中**：始終用 `act()` 包裝 `fireEvent` 呼叫，以確保 React 狀態更新得到正確處理。
   - **使用 `query` 方法進行不存在檢查**：當預期某個元素「不應存在」時，請使用 `queryBy*` 方法（而非 `getBy*`）。
   - **測試名稱必須以 "should" 開頭**：所有測試名稱應遵循 `it("should ...")` 模式。
   - **模擬外部依賴**：檢查 `setupTests.ts` 以獲取全域 Mock，並根據需要模擬子組件/網路呼叫。
   - **正確組織測試結構**：
     - 第一個測試應驗證組件是否成功渲染。
     - 後續測試應專注於功能和使用者互動。
     - 對於尚未被 await 的非同步操作，請使用 `waitFor`。
   - **避免使用 `querySelector`**：優先使用 React Testing Library 的查詢方法，而非直接操作 DOM。

### 重要模式

1. **功能/工具呼叫 (Function/Tool Calling)**：
   - LiteLLM 將不同供應商的工具呼叫標準化。
   - 以 OpenAI 格式為標準，並為其他供應商進行轉換。
   - 參見 `litellm/llms/anthropic/chat/transformation.py` 以瞭解複雜的工具處理。

2. **串流 (Streaming)**：
   - 所有供應商應盡可能支援串流。
   - 在不同供應商之間使用一致的 Chunk 格式。
   - 同時處理同步和非同步串流。

3. **錯誤處理**：
   - 使用供應商特定的異常類別。
   - 在不同供應商之間保持一致的錯誤格式。
   - 包含正確的重試邏輯和回退機制。

4. **配置**：
   - 同時支援環境變數和程式化配置。
   - 為供應商配置使用 `BaseConfig` 類別。
   - 允許動態傳遞參數。

## 代理伺服器 (AI 閘道器)

代理伺服器是提供以下功能的關鍵組件：
- 身份驗證與授權。
- 速率限制與預算管理。
- 跨多個模型/部署的負載平衡。
- 可觀測性與日誌紀錄。
- 管理員儀表板 UI。
- 企業版功能。

關鍵檔案：
- `litellm/proxy/proxy_server.py` - 主要伺服器實作
- `litellm/proxy/auth/` - 身份驗證邏輯
- `litellm/proxy/management_endpoints/` - 管理員 API 端點

**資料庫 (Proxy)**：請使用 Prisma 模型方法 (`prisma_client.db.<model>.upsert`, `.find_many`, `.find_unique` 等)，**不要**使用原始 SQL (`execute_raw`/`query_raw`)。詳情請參見「常見陷阱」。

## MCP (模型上下文協定) 支援

LiteLLM 為代理工作流支援 MCP：
- 用於工具呼叫的 MCP 伺服器整合。
- OpenAI 和 MCP 工具格式之間的轉換。
- 支援外部 MCP 伺服器（Zapier, Jira, Linear 等）。
- 參見 `litellm/experimental_mcp_client/` 和 `litellm/proxy/_experimental/mcp_server/`。

## 執行腳本

使用 `poetry run python script.py` 在專案環境中執行 Python 腳本（適用於非測試檔案）。

## GITHUB 範本

開啟 Issue 或 Pull Request 時，請遵循以下範本：

### Bug 報告 (`.github/ISSUE_TEMPLATE/bug_report.yml`)
- 描述實際發生的情況與預期行為。
- 包含相關的日誌輸出。
- 註明 LiteLLM 版本。
- 標註您是否屬於 ML Ops 團隊（有助於優先級排序）。

### 功能請求 (`.github/ISSUE_TEMPLATE/feature_request.yml`)
- 清晰描述功能。
- 用具體範例說明動機和使用情境。

### Pull Request (`.github/pull_request_template.md`)
- 在 `tests/litellm/` 中加入至少 1 個測試。
- 確保 `make test-unit` 通過。


## 測試注意事項

1. **供應商測試**：盡可能針對真實的供應商 API 進行測試。
2. **Proxy 測試**：包含身份驗證、速率限制和路由測試。
3. **效能測試**：針對高吞吐量情境進行負載測試。
4. **整合測試**：包含工具呼叫在內的端到端工作流。

## 文件

- 保持文件與程式碼變更同步。
- 新增供應商時更新相關供應商文件。
- 為新功能提供程式碼範例。
- 更新變更日誌 (Changelog) 和發布說明。

## 安全注意事項

- 安全地處理 API 金鑰。
- 驗證所有輸入，特別是 Proxy 端點。
- 考慮速率限制和防止濫用。
- 遵循身份驗證的安全最佳實踐。

## 企業版功能

- 部分功能僅限企業版使用。
- 查看 `enterprise/` 目錄以獲取企業版專屬程式碼。
- 保持開源版與企業版之間的相容性。

## 應避免的常見陷阱

1. **破壞性變更 (Breaking Changes)**：LiteLLM 有許多使用者 —— 應避免破壞現有的 API。
2. **供應商特性**：每個供應商都有獨特的怪癖 —— 請正確處理它們。
3. **速率限制**：在測試中尊重供應商的速率限制。
4. **記憶體使用**：在串流情境下注意記憶體使用量。
5. **依賴關係**：保持最小且合理的依賴關係。
6. **UI/後端契約不匹配**：在 UI 中新增實體類型時，務必檢查後端端點接受的是單個值還是陣列。相應地匹配 UI 控制項（單選 vs. 多選），以避免無意中丟棄使用者的選擇。
7. **新實體類型缺乏測試**：新增實體類型（例如在 `EntityUsage`, `UsageViewSelect` 中）時，務必在現有測試檔案中加入相應測試，並更新任何圖示/組件 Mock。
8. **Proxy DB 程式碼中的原始 SQL**：**不要**在 Proxy 資料庫存取中使用 `execute_raw` 或 `query_raw`。請使用 Prisma 模型方法（例如 `prisma_client.db.litellm_tooltable.upsert()`, `.find_many()`, `.find_unique()`），以便行為與 Schema 保持一致、用戶端在測試中可被 Mock，並避免手寫 SQL 的陷阱（參數順序、型別轉換、Schema 偏移）。

9. **切勿硬編碼模型特定標籤**：將模型特定的能力標籤放在 `model_prices_and_context_window.json` 中，並透過 `get_model_info`（或現有的輔助函式如 `supports_reasoning`）讀取。這可以防止使用者在每次新模型支援某項功能時都需要升級 LiteLLM。

   **錯誤範例**（硬編碼模型檢查）：

   ```python
   @staticmethod
   def _is_effort_supported_model(model: str) -> bool:
       """檢查模型是否支援 output_config.effort 參數..."""
       model_lower = model.lower()
       if AnthropicConfig._is_claude_4_6_model(model):
           return True
       return any(
           v in model_lower for v in ("opus-4-5", "opus_4_5", "opus-4.5", "opus_4.5")
       )
   ```

   **正確範例**（由配置驅動或讀取配置的輔助函式）：

   ```python
   if (
       "claude-3-7-sonnet" in model
       or AnthropicConfig._is_claude_4_6_model(model)
       or supports_reasoning(
           model=model,
           custom_llm_provider=self.custom_llm_provider,
       )
   ):
       ...
   ```

   使用 `supports_reasoning`（從 `model_prices_and_context_window.json` / `get_model_info` 讀取）等輔助函式，可以讓未來的模型更新在無需更改程式碼的情況下「直接運作」。

10. **絕不要在快取逐出時關閉 HTTP/SDK 用戶端**：不要在 `LLMClientCache._remove_key()` 或任何快取逐出路徑中加入 `close()`, `aclose()` 或 `create_task(close_fn())`。被逐出的用戶端可能仍被正在進行的請求持有；關閉它們會導致生產環境在快取 TTL（1 小時）過期後出現 `RuntimeError: Cannot send a request, as the client has been closed.`。連接清理在關機時由 `close_litellm_async_clients()` 統一處理。詳情請參見 PR #22247。

## 輔助資源

- 主要文件：https://docs.litellm.ai/
- 供應商特定文件位於 `docs/my-website/docs/providers/`
- 用於測試 Proxy 功能的管理員 UI

## 如有疑問

- 遵循程式碼庫中的現有模式。
- 參考類似的供應商實作。
- 確保全面的測試覆蓋。
- 適當地更新文件。
- 考慮對向後相容性的影響。

## Cursor Cloud 特定指令

### 環境

- Poetry 安裝於 `~/.local/bin`；更新腳本會確保其在 `PATH` 中。
- 已預裝 Python 3.12 和 Node 22。
- 虛擬環境位於 `~/.cache/pypoetry/virtualenvs/`。

### 執行 Proxy 伺服器

使用配置文件啟動 Proxy：

```bash
poetry run litellm --config dev_config.yaml --port 4000
```

Proxy 約需 15-20 秒完全啟動（啟動時會執行 Prisma 遷移）。發送請求前請等待 `/health` 返回正常。若無 PostgreSQL `DATABASE_URL`，Proxy 將連接到 `litellm-proxy-extras` 套件中內嵌的預設 Neon 開發資料庫。

### 執行測試

有關標準指令，請參閱 `CLAUDE.md` 和 `Makefile`。關鍵注意事項：

- 必須安裝 `psycopg-binary` (`poetry run pip install psycopg-binary`)，因為 `pytest-postgresql` 插件需要它，而 Lock 檔案僅包含 `psycopg`（無 binary）。
- 必須安裝 `openapi-core` (`poetry run pip install openapi-core`) 以進行 `tests/test_litellm/interactions/` 中的 OpenAPI 合規性測試。
- **不支援** `--timeout` pytest 標記；請勿傳遞此參數。
- 單元測試：`poetry run pytest tests/test_litellm/ -x -vv -n 4`
- Black `--check` 可能會報告預先存在的格式問題；這不會阻礙測試執行。
- 若 `poetry install` 失敗並顯示 "pyproject.toml changed significantly..."，請先執行 `poetry lock` 重新產生 Lock 檔案。

### Lint

```bash
cd litellm && poetry run ruff check .
```

Ruff 是主要的快速 Linter。若要執行全套 Lint（包括 MyPy, Black, 循環導入檢查），請依據 `CLAUDE.md` 執行 `make lint`。

### UI 儀表板開發

- UI 位於 `ui/litellm-dashboard/`。在該目錄中執行 `npm run dev` 即可啟動連接埠 3000 的 Next.js 開發伺服器。
- 連接埠 4000 的 Proxy 提供的是 `litellm/proxy/_experimental/out/` 中的**預編譯**靜態 UI。修改 UI 程式碼後，必須在儀表板目錄中執行 `npm run build` 並複製輸出：`cp -r ui/litellm-dashboard/out/* litellm/proxy/_experimental/out/`，以便 Proxy 提供更新後的 UI。
- 用作供應商標誌的 SVG（透過 `<img>` 標籤載入）**不得**使用 `fill="currentColor"` —— 請替換為顯式顏色如 `#000000` 或使用 lobehub 圖示的 `-color` 變體，因為 CSS 顏色繼承在 `<img>` 元素內部無效。
- 供應商標誌位於 `ui/litellm-dashboard/public/assets/logos/` (原始碼) 和 `litellm/proxy/_experimental/out/assets/logos/` (預編譯)。這兩個位置都必須包含該檔案，才能在開發模式和 Proxy 提供模式下正常運作。
- UI Vitest 測試：`cd ui/litellm-dashboard && npx vitest run`
