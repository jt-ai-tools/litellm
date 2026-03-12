# GEMINI.md

本文件為 Gemini 在本倉庫中處理程式碼時提供指引。

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

### 測試策略
- 單元測試位於 `tests/test_litellm/`
- 每個供應商的整合測試位於 `tests/llm_translation/`
- Proxy 測試位於 `tests/proxy_unit_tests/`
- 負載測試位於 `tests/load_tests/`

### 資料庫遷移
- Prisma 處理 Schema 遷移
- 遷移檔案由 `prisma migrate dev` 自動產生
- 務必針對 PostgreSQL 和 SQLite 進行遷移測試

### 企業版功能
- 企業版專屬程式碼位於 `enterprise/` 目錄
- 透過環境變數啟用選用功能
- 企業版具備獨立的授權與身份驗證機制
