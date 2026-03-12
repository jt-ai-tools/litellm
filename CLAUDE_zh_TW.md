# CLAUDE.md

本文件為 Claude Code (claude.ai/code) 在本倉庫中處理程式碼時提供指引。

## 開發指令

### 安裝
- `make install-dev` - 安裝核心開發依賴
- `make install-proxy-dev` - 安裝具備完整功能的 Proxy 開發依賴
- `make install-test-deps` - 安裝所有測試依賴

### 測試
- `make test` - 執行所有測試
- `make test-unit` - 使用 4 個並行工作線程執行單元測試 (tests/test_litellm)
- `make test-integration` - 執行整合測試（不含單元測試）
- `pytest tests/` - 直接執行 pytest

### 程式碼品質
- `make lint` - 執行所有 Lint 檢查（Ruff, MyPy, Black, 循環導入, 導入安全性）
- `make format` - 套用 Black 程式碼格式化
- `make lint-ruff` - 僅執行 Ruff Lint
- `make lint-mypy` - 僅執行 MyPy 型別檢查

### 單一測試檔案
- `poetry run pytest tests/path/to/test_file.py -v` - 執行特定測試檔案
- `poetry run pytest tests/path/to/test_file.py::test_function -v` - 執行特定測試函式

### 執行腳本
- `poetry run python script.py` - 執行 Python 腳本（用於非測試檔案）

### GitHub Issue & PR 範本
貢獻專案時，請使用相應的範本：

**Bug 報告** (`.github/ISSUE_TEMPLATE/bug_report.yml`)：
- 描述實際發生的情況與預期行為
- 包含相關的日誌輸出
- 註明您的 LiteLLM 版本

**功能請求** (`.github/ISSUE_TEMPLATE/feature_request.yml`)：
- 清晰描述功能
- 說明動機與使用情境

**Pull Requests** (`.github/pull_request_template.md`)：
- 在 `tests/litellm/` 中加入至少 1 個測試
- 確保 `make test-unit` 通過

## 架構總覽

LiteLLM 是一個統一的 100+ 種 LLM 供應商介面，包含兩個主要組件：

### 核心函式庫 (`litellm/`)
- **主要入口點**：`litellm/main.py` - 包含核心的 completion() 函式
- **供應商實作**：`litellm/llms/` - 每個供應商都有自己的子目錄
- **路由器系統**：`litellm/router.py` + `litellm/router_utils/` - 負載平衡與回退邏輯
- **型別定義**：`litellm/types/` - Pydantic 模型與型別提示
- **整合**：`litellm/integrations/` - 第三方可觀測性、快取、日誌
- **快取**：`litellm/caching/` - 多種快取後端（Redis, 記憶體, S3 等）

### Proxy 伺服器 (`litellm/proxy/`)
- **主要伺服器**：`proxy_server.py` - FastAPI 應用程式
- **身份驗證**：`auth/` - API 金鑰管理、JWT、OAuth2
- **資料庫**：`db/` - 支援 PostgreSQL/SQLite 的 Prisma ORM
- **管理端點**：`management_endpoints/` - 用於金鑰、團隊、模型的管理員 API
- **直通端點**：`pass_through_endpoints/` - 供應商特定的 API 轉發
- **護欄 (Guardrails)**：`guardrails/` - 安全性與內容過濾鉤子
- **UI 儀表板**：由 `_experimental/out/` 提供 (Next.js 構建)

## 關鍵模式

### 供應商實作
- 供應商繼承自 `litellm/llms/base.py` 中的基礎類別
- 每個供應商都有用於輸入/輸出格式化的轉換函式
- 支援同步與非同步操作
- 處理串流回應與工具呼叫

### 錯誤處理
- 將供應商特定的異常映射到與 OpenAI 相容的錯誤
- 由路由器系統處理回退邏輯
- 透過 `litellm/_logging.py` 進行全面的日誌紀錄

### 配置
- Proxy 伺服器的 YAML 配置文件（參見 `proxy/example_config_yaml/`）
- 用於 API 金鑰與設定的環境變數
- 透過 Prisma 管理資料庫 Schema (`proxy/schema.prisma`)

## 開發備註

### 程式碼風格
- 使用 Black 格式化工具、Ruff Linter、MyPy 型別檢查器
- 使用 Pydantic v2 進行資料驗證
- 全程使用 Async/await 模式
- 所有公開 API 皆需型別提示
- **避免在方法內部導入 (Imports)** — 請將所有導入放在檔案頂部（模組級別）。在函式/方法內部進行內聯導入會使依賴關係難以追蹤並破壞可讀性。唯一的例外是為了避免絕對必要的循環導入。

### 測試策略
- 單元測試位於 `tests/test_litellm/`
- 每個供應商的整合測試位於 `tests/llm_translation/`
- Proxy 測試位於 `tests/proxy_unit_tests/`
- 負載測試位於 `tests/load_tests/`
- **新增實體類型或功能時務必加入測試** — 如果現有的測試檔案已涵蓋其他實體類型，請為新實體加入相應的測試。

### UI / 後端一致性
- 將新的 UI 實體類型連接到現有的後端端點時，請驗證後端 API 契約（單一值 vs. 陣列、必填 vs. 選填參數）並確保 UI 控制項匹配 —— 例如，當後端僅接受單一值時，請使用單選下拉選單，而非多選。

### MCP OAuth / OpenAPI 傳輸映射
- `TRANSPORT.OPENAPI` 是一個僅限 UI 的概念。後端僅接受 `"http"`, `"sse"`, 或 `"stdio"`。在進行任何 API 呼叫（包括 OAuth 前的臨時會話呼叫）之前，務必將其映射為 `"http"`。
- FastAPI 驗證錯誤會將 `detail` 作為 `{loc, msg, type}` 物件的陣列返回。錯誤提取器必須處理：陣列（映射 `.msg`）、字串、嵌套的 `{error: string}` 以及回退機制。
- 當 MCP 伺服器已儲存 `authorization_url` 時，請跳過 OAuth 發現 (`_discovery_metadata`) —— OpenAPI MCP 的伺服器 URL 是規格檔案，而非 API 基礎路徑，抓取它會導致超時。
- `/authorize` 端點中的 `client_id` 應為選填 —— 如果伺服器在憑證中已有儲存的 `client_id`，請直接使用。切勿要求呼叫者重複提供。

### MCP 憑證儲存
- OAuth 憑證與 BYOK 憑證共享 `litellm_mcpusercredentials` 資料表，透過 JSON Payload 中的 `"type"` 欄位區分（`"oauth2"` vs. 普通字串）。
- 刪除 OAuth 憑證時，請先檢查類型，以免誤刪相同 `(user_id, server_id)` 對應的 BYOK 憑證。
- 始終將原始的 `expires_at` 時間戳傳遞給客戶端 —— 切勿為已過期的憑證將其設置為 `None`。讓前端根據時間戳計算並顯示「已過期」狀態。
- 在憑證刪除端點捕捉「已刪除」異常時，請使用 `RecordNotFoundError`（而非空的 `except Exception`）。

### 瀏覽器儲存安全 (UI)
- 絕不要將 LiteLLM 存取權杖 (Access Tokens) 或 API 金鑰寫入 `localStorage` —— 僅限使用 `sessionStorage`。`localStorage` 在瀏覽器關閉後仍會存在，且可被任何注入的腳本 (XSS) 讀取。
- 共享的工具函式（如 `extractErrorMessage`）應置於 `src/utils/` —— 絕不要在 Hook 中內聯定義或在多個檔案中重複定義。

### 資料庫遷移
- Prisma 處理 Schema 遷移
- 遷移檔案由 `prisma migrate dev` 自動產生
- 務必針對 PostgreSQL 和 SQLite 進行遷移測試

### Proxy 資料庫存取
- **不要為 Proxy DB 操作編寫原始 SQL**。請使用 Prisma 模型方法，而非 `execute_raw` / `query_raw`。
- 使用產生的用戶端：`prisma_client.db.<model>`（例如 `litellm_tooltable`, `litellm_usertable`），並根據需要使用 `.upsert()`, `.find_many()`, `.find_unique()`, `.update()`, `.update_many()`。這可以避免 Schema 與用戶端不一致、保持程式碼可透過 Simple Mocks 進行測試，並與支出日誌及其他 Proxy 程式碼中的模式保持一致。
- **禁止 N+1 查詢**。絕不要在迴圈內部查詢資料庫。請使用 `{"in": ids}` 進行批量抓取，並在記憶體中分發。
- **批量寫入**。使用 `create_many` / `update_many` / `delete_many` 代替個別呼叫（這些方法僅返回計數；`update_many` / `delete_many` 在查無列時會靜默不執行）。當多個獨立寫入針對同一張資料表（例如在 `batch_()` 中）時，請按主鍵排序以避免死鎖。
- **將運算推給資料庫**。請在 SQL 中進行過濾、排序、分組和聚合，而非 Python。驗證 Prisma 是否產生了預期的 SQL —— 例如：優先使用 `group_by` 而非在客戶端處理的 `find_many(distinct=...)`。
- **限制大型結果集**。Prisma 會在記憶體中具現化完整結果。對於超過 ~10 MB 的結果，請使用 `take` / `skip` 或 `cursor` / `take` 進行分頁，且務必帶有顯式的 `order`。優先使用基於游標 (Cursor-based) 的分頁（`skip` 是 O(n)）。不要對原本就很小的結果集進行分頁。
- **在寬資料表上限制抓取的欄位**。使用 `select` 僅抓取需要的欄位 —— 這會返回部分物件，因此下游程式碼不得存取未選取的欄位。
- **檢查索引覆蓋率**。對於新增或修改的查詢，請檢查 `schema.prisma` 是否有支持的索引。優先擴展現有索引（例如 `@@index([a])` → `@@index([a, b])`），而非新增索引，除非是 `@@unique`。僅為大型或頻繁的查詢新增索引。
- **保持 Schema 檔案同步**。將 Schema 變更套用到所有 `schema.prisma` 複本（包括 `schema.prisma`, `litellm/proxy/`, `litellm-proxy-extras/`, 以及用於 SpendLogs 的 `litellm-js/spend-logs/`），並在 `litellm-proxy-extras/litellm_proxy_extras/migrations/` 下進行遷移。

### 企業版功能
- 企業版專屬程式碼位於 `enterprise/` 目錄
- 透過環境變數啟用選用功能
- 企業版具備獨立的授權與身份驗證機制

### HTTP 用戶端快取安全
- **絕不要在快取逐出時關閉 HTTP/SDK 用戶端。** `LLMClientCache._remove_key()` 不得在被逐出的用戶端上呼叫 `close()` / `aclose()` —— 它們可能仍被正在進行的請求使用。這樣做會導致在 1 小時 TTL 過期後出現 `RuntimeError: Cannot send a request, as the client has been closed.`。清理工作應在關機時透過 `close_litellm_async_clients()` 統一處理。

### 疑難排解：Proxy 重啟後 DB Schema 不同步
`litellm-proxy-extras` 在啟動時會使用**其自身**捆綁的遷移檔案執行 `prisma migrate deploy`，這可能會落後於當前工作樹中的 Schema 變更。症狀：`Unknown column`, `Invalid prisma invocation` 或新欄位數據缺失。

**診斷**：在 psql 中執行 `\d "TableName"` 並與 `schema.prisma` 對比 —— 缺失欄位即可確認問題。

**修復選項**：
1. **建立 Prisma 遷移**（永久性） — 在工作樹中執行 `prisma migrate dev --name <description>`。產生的檔案將在下次啟動時被 `prisma migrate deploy` 拾取。
2. **手動套用於本地開發** — 每次 Proxy 啟動後執行 `psql -d litellm -c "ALTER TABLE ... ADD COLUMN IF NOT EXISTS ..."`。這對開發環境有效，但不適用於生產環境。
3. **更新 litellm-proxy-extras** — 如果是從 PyPI 安裝該套件，其遷移目錄必須包含新檔案。請更新套件或在下個版本發布前手動執行遷移。
