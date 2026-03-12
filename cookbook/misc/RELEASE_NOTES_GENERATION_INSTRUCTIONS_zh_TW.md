# LiteLLM Release Notes 生成指南

本文件為 AI agents 提供詳細指令，說明如何按照既定的格式與風格生成 LiteLLM 的 release notes。

## 必備輸入資訊

1. **Release 版本** (例如：`v1.77.3-stable`)
2. **PR Diff/Changelog** - 包含標題與貢獻者的 PR 清單
3. **前一版本的 Commit Hash** - 用於比較模型價格 (model pricing) 的變更
4. **參考 Release Notes** - 使用最近的穩定版本 (v1.76.3-stable, v1.77.2-stable) 作為模板，以確保格式一致

## 逐步執行流程

### 1. 初始設定與分析

```bash
# 檢查 git diff 以了解模型價格變更
git diff <previous_commit_hash> HEAD -- model_prices_and_context_window.json
```

**分析重點：**
- 新增的模型 (尋找新條目)
- 已棄用的模型 (尋找被刪除的條目)
- 價格更新 (尋找成本變更)
- 功能支援變更 (tool calling, reasoning 等)

### 2. Release Notes 結構

請參考最近的穩定版本 (v1.76.3-stable, v1.77.2-stable, v1.77.5-stable) 遵循以下結構：

```markdown
---
title: "v1.77.X-stable - [Key Theme]"
slug: "v1-77-X"
date: YYYY-MM-DDTHH:mm:ss
authors: [standard author block]
hide_table_of_contents: false
---

## Deploy this version
[Docker and pip installation tabs]

## Key Highlights
[3-5 個主要功能的列點 - 優先考量 MCP OAuth 2.0, scheduled key rotations, 以及重大模型更新]

## New Providers and Endpoints

### New Providers
[包含 Provider, Supported Endpoints, Description 欄位的表格]

### New LLM API Endpoints
[選填：新端點表格，包含 Endpoint, Method, Description, Documentation 欄位]

## New Models / Updated Models
#### New Model Support
[模型價格表格]

#### Features
[依 provider 分類的功能]

### Bug Fixes
[依 provider 分類的錯誤修復]

## LLM API Endpoints
#### Features
[依 API 類型分類的功能]

#### Bugs
[一般錯誤修復]

## Management Endpoints / UI
#### Features
[UI 與管理功能 - 依功能分組，例如 Proxy CLI Auth, Virtual Keys, Models + Endpoints]

#### Bugs
[與管理相關的錯誤修復]

## AI Integrations

### Logging
[依 provider 分類的 Logging 整合，包含正確的文件連結，並包含 General 子章節]

### Guardrails
[Guardrail 相關的功能與修復]

### Prompt Management
[Prompt 管理整合，例如 BitBucket]

### Secret Managers
[Secret manager 整合 - AWS, HashiCorp Vault, CyberArk 等]

## Spend Tracking, Budgets and Rate Limiting
[成本追蹤, service tier pricing, rate limiting 改進]

## MCP Gateway
[MCP 相關功能, OAuth 2.0, 設定改進]

## Performance / Loadbalancing / Reliability improvements
[基礎設施改進, 記憶體修復, 效能最佳化]

## Documentation Updates
[文件改進, 指南, 修正 - 獨立章節以提高能見度]

## New Contributors
[首次貢獻者名單]

## Full Changelog
[指向 GitHub comparison 的連結]
```

### 3. 分類規則

**Performance Improvements (效能改進):**
- RPS 提升
- 記憶體最佳化
- CPU 使用率最佳化
- Timeout 控制
- Worker 設定
- 記憶體洩漏修復
- Cache 效能改進
- 資料庫連線管理
- 依賴管理 (fastuuid 等)
- 設定管理

**New Models/Updated Models (新模型/更新模型):**
- 從 model_prices_and_context_window.json 的 diff 中擷取
- 建立包含以下欄位的表格：Provider, Model, Context Window, Input Cost, Output Cost, Features
- **結構：**
  - `#### New Model Support` - 價格表格
  - `#### Features` - 依 provider 分類並附上文件連結
  - `### Bug Fixes` - 特定 provider 的錯誤修復
  - `#### New Provider Support` - 重大的新供應商整合
- 依 provider 分組並附上正確的文件連結：`**[Provider Name](../../docs/providers/[provider])**`
- 每個 provider 下方使用列點列出多項功能
- 清確區分 Features 與 Bug Fixes

**LLM API Endpoints:**
- **結構：**
  - `#### Features` - 依 API 類型分類 (Responses API, Batch API 等)
  - `#### Bugs` - **General** 類別下的一般錯誤修復
- **API 類別：**
  - Responses API
  - Batch API  
  - CountTokens API
  - Images API
  - Video Generation (如果適用)
  - General (雜項改進)
- 為每個 API 類型使用正確的文件連結

**UI/Management:**
- 身份驗證 (Authentication) 變更
- Dashboard 改進
- 團隊管理
- 金鑰管理 (Key management)
- Proxy CLI 身份驗證與改進
- Virtual key 管理與定期輪換 (scheduled rotations)
- SSO 設定修復
- 管理員設定更新
- 管理路由與端點

**AI Integrations:**
- **結構：**
  - `### Logging` - 依整合供應商分類並附上正確連結，包含 **General** 子章節
  - `### Guardrails` - Guardrail 相關功能與修復
  - `### Prompt Management` - Prompt 管理整合
  - `### Secret Managers` - Secret manager 整合
- **Logging 類別：**
  - **[DataDog](../../docs/proxy/logging#datadog)** - 群組所有 DataDog 相關變更
  - **[Langfuse](../../docs/proxy/logging#langfuse)** - Langfuse 特定功能
  - **[Prometheus](../../docs/proxy/logging#prometheus)** - 監控改進
  - **[PostHog](../../docs/observability/posthog)** - 觀測性整合
  - **[SQS](../../docs/proxy/logging#sqs)** - SQS logging 功能
  - **[Opik](../../docs/proxy/logging#opik)** - Opik 整合改進
  - **[Arize Phoenix](../../docs/observability/arize_phoenix)** - Arize Phoenix 整合
  - **General** - 雜項 logging 功能，如回呼控制 (callback controls)、敏感資料遮罩
  - 其他附有正確連結的 logging 供應商
- **Guardrail 類別：**
  - LakeraAI, Presidio, Noma, Grayswan, IBM Guardrails 以及其他 guardrail 供應商
- **Prompt Management:**
  - BitBucket, GitHub 以及其他 prompt 管理整合
  - Prompt 版本控制、測試與 UI 功能
- **Secret Managers:**
  - **[AWS Secrets Manager](../../docs/secret_managers)** - AWS secret manager 功能
  - **[HashiCorp Vault](../../docs/secret_managers)** - Vault 整合
  - **[CyberArk](../../docs/secret_managers)** - CyberArk 整合
  - **General** - 跨 secret manager 的功能
- 每個 provider 下方使用列點列出多項功能
- 清楚區隔 logging, guardrails, prompt management 與 secret managers

### 4. 文件連結策略

**在以下情況連結到文件：**
- 新增 Provider 支援
- 重大功能新增
- API 端點變更
- 整合功能新增

**連結格式：** `../../docs/[category]/[specific_doc]`

**常用文件路徑：**
- `../../docs/providers/[provider]` - 特定 Provider 文件
- `../../docs/image_generation` - 圖片生成
- `../../docs/video_generation` - 影片生成 (如果存在)
- `../../docs/response_api` - Responses API
- `../../docs/proxy/logging` - Logging 整合
- `../../docs/proxy/guardrails` - Guardrails
- `../../docs/pass_through/[provider]` - Passthrough 端點

### 5. 模型表格生成

根據 git diff 分析，建立如下表格：

```markdown
| Provider | Model | Context Window | Input ($/1M tokens) | Output ($/1M tokens) | Features |
| -------- | ----- | -------------- | ------------------- | -------------------- | -------- |
| OpenRouter | `openrouter/openai/gpt-4.1` | 1M | $2.00 | $8.00 | Chat completions with vision |
```

**從 JSON 擷取資訊：**
- `max_input_tokens` → Context Window
- `input_cost_per_token` × 1,000,000 → Input cost
- `output_cost_per_token` × 1,000,000 → Output cost
- `supports_*` 欄位 → Features
- 生成模型的特殊價格欄位 (每張圖片, 每秒)

### 6. PR 分類邏輯

**依 PR 標題關鍵字：**
- `[Perf]`, `Performance`, `RPS` → Performance Improvements
- `[Bug]`, `[Bug Fix]`, `Fix` → Bug Fixes 章節
- `[Feat]`, `[Feature]`, `Add support` → Features 章節
- `[Docs]` → Documentation Updates 章節
- Provider 名稱 (Gemini, OpenAI 等) → 在 provider 下分組
- `MCP`, `oauth`, `Model Context Protocol` → MCP Gateway
- `service_tier`, `priority`, `cost tracking` → Spend Tracking, Budgets and Rate Limiting

**依 PR 內容分析：**
- 新模型新增 → New Models 章節
- UI 變更 → Management Endpoints/UI
- Logging/observability → Logging/Guardrail/Prompt Management Integrations
- Rate limiting/budgets → Spend Tracking, Budgets and Rate Limiting
- 身份驗證 (Authentication) → Management Endpoints/UI
- MCP 相關變更 → MCP Gateway
- 文件更新 → Documentation Updates
- 效能/記憶體修復 → Performance/Loadbalancing/Reliability improvements

**特殊分類規則：**
- **Service tier pricing** (OpenAI priority/flex) → Spend Tracking 章節 (非 provider 功能)
- **Logging 中的成本細分 (Cost breakdown)** → Spend Tracking 章節
- **MCP 設定/OAuth** → MCP Gateway (非一般 Proxy 改進)
- **所有文件 PR** → Documentation Updates 章節以提高能見度
- **Callback controls/logging 功能** → AI Integrations > Logging > General
- **Secret manager 功能** → AI Integrations > Secret Managers
- **影片生成基於標籤的路由 (tag-based routing)** → LLM API Endpoints > Video Generation API

### 7. 寫作風格指南

**語氣：**
- 專業且平易近人
- 專注於對使用者的影響
- 清楚標出重大變更 (breaking changes)
- 使用主動語態

**格式：**
- 使用一致的 markdown 格式
- 包含 PR 連結：`[PR #XXXXX](https://github.com/BerriAI/litellm/pull/XXXXX)`
- 使用程式碼區塊提供設定範例
- 粗體顯示重要術語與章節標題

**警告/注意事項：**
- 為重大變更加入警告方塊 (warning boxes)
- 需要時包含遷移指令 (migration instructions)
- 為預設值變更提供覆寫選項

### 8. 品質檢查

**定稿前：**
- 驗證所有 PR 連結皆可運作
- 檢查文件連結是否有效
- 確保模型價格準確
- 確認 provider 名稱一致
- 檢查拼字與格式錯誤
- **按章節統計 PR 數量** - 提供最終計數，例如：
  ```
  ## MM/DD/YYYY
  * New Models / Updated Models: XX
  * LLM API Endpoints: XX
  * Management Endpoints / UI: XX
  * Logging / Guardrail / Prompt Management Integrations: XX
  * Spend Tracking, Budgets and Rate Limiting: XX
  * MCP Gateway: XX
  * Performance / Loadbalancing / Reliability improvements: XX
  * Documentation Updates: XX
  ```

### 9. 常用模式

**效能變更：**
```markdown
- **+400 RPS 效能提升** - 描述 - [PR #XXXXX](link)
```

**新模型：**
務必包含價格表格與功能亮點

**重大變更 (Breaking Changes)：**
```markdown
:::warning
此版本有一個已知問題...
:::
```

**Provider 功能 (New Models / Updated Models 章節)：**
```markdown
#### Features

- **[Provider Name](../../docs/providers/provider)**
    - 功能描述 - [PR #XXXXX](link)
    - 另一項功能描述 - [PR #YYYYY](link)
```

**API 功能 (LLM API Endpoints 章節)：**
```markdown
#### Features

- **[API Name](../../docs/api_path)**
    - 功能描述 - [PR #XXXXX](link)
    - 另一項功能 - [PR #YYYYY](link)
- **General**
    - 雜項改進 - [PR #ZZZZZ](link)
```

**整合功能 (Logging / Guardrail Integrations 章節)：**
```markdown
#### Features

- **[Integration Name](../../docs/proxy/logging#integration)**
    - 功能描述 - [PR #XXXXX](link)
    - 錯誤修復描述 - [PR #YYYYY](link)
```

**錯誤修復模式：**
```markdown
### Bug Fixes

- **[Provider/Component Name](../../docs/providers/provider)**
    - 錯誤修復描述 - [PR #XXXXX](link)
```

### 10. 缺失文件檢查

**審核是否缺少文件：**
- 新 Provider 缺少文件
- 新 API 端點缺少範例
- 複雜功能缺少指南
- 整合設定指令

**標記文件需求：**
- 新 Provider 整合
- 重大 API 變更
- 複雜的設定選項
- 遷移需求

### 11. 新章節與類別 (v1.77.5 新增)

**MCP Gateway 章節：**
- 所有與 MCP 相關的變更皆在此處 (非一般 Proxy 改進)
- OAuth 2.0 流程改進
- MCP 設定與工具
- 伺服器管理功能

**Spend Tracking, Budgets and Rate Limiting 章節：**
- Service tier pricing (OpenAI priority/flex pricing)
- 成本追蹤與細分功能
- Rate limiting 改進 (Parallel Request Limiter v3)
- 優先權保留 (Priority reservation) 修復
- Rate limiting 的元資料 (metadata) 處理

**Documentation Updates 章節：**
- 為所有文件改進建立獨立章節
- 包含 provider 文件修復
- 模型參考更新
- 新指南與教學
- 文件修正與說明
- 這讓文件變更能獲得應有的關注

**Management Endpoints / UI 分組：**
- 將相關功能分組至子類別：
  - **Proxy CLI Auth** - CLI 身份驗證改進
  - **Virtual Keys** - 金鑰輪換與管理
  - **Models + Endpoints** - Provider 與端點管理

**AI Integrations 章節擴充：**
- 從 "Logging / Guardrail / Prompt Management Integrations" 更名為 "AI Integrations"
- 包含四個主要子章節的結構：
  - **Logging** - 包含 **General** 子章節提供雜項 logging 功能
  - **Guardrails** - 與 logging 功能區隔
  - **Prompt Management** - BitBucket, GitHub 整合, 版本控制功能
  - **Secret Managers** - AWS, HashiCorp Vault, CyberArk 等

**New Providers and Endpoints 章節：**
- 在 Key Highlights 之後、New Models / Updated Models 之前加入此章節
- 包含以下表格：
  - **New Providers** - Provider 名稱, 支援端點, 描述
  - **New LLM API Endpoints** (選填) - Endpoint, method, description, 文件連結
- 僅包含重大的新供應商整合，不包含微小的 provider 更新
- **重要**：新增供應商時，亦須更新 repository 根目錄下的 `provider_endpoints_support.json` (見第 13 節)

### 12. 章節標題計數

**務必在以下章節標題中包含計數：**
- **New Providers** - 在括號中加入計數：`### New Providers (X new providers)`
- **New LLM API Endpoints** - 在括號中加入計數：`### New LLM API Endpoints (X new endpoints)`
- **New Model Support** - 在括號中加入計數：`#### New Model Support (X new models)`

**格式：**
```markdown
### New Providers (4 new providers)

| Provider | Supported LiteLLM Endpoints | Description |
| -------- | --------------------------- | ----------- |
...

### New LLM API Endpoints (2 new endpoints)

| Endpoint | Method | Description | Documentation |
| -------- | ------ | ----------- | ------------- |
...

#### New Model Support (32 new models)

| Provider | Model | Context Window | Input ($/1M tokens) | Output ($/1M tokens) | Features |
| -------- | ----- | -------------- | ------------------- | -------------------- | -------- |
...
```

**計數規則：**
- 計算表格中的每一列 (不含標題列)
- 對於模型，計算價格表格中的每個模型條目
- 對於供應商，計算新增的每個供應商
- 對於端點，計算新增的每個 API 端點

### 13. 更新 provider_endpoints_support.json

**當新增供應商或端點時，您「必須」同時更新 repository 根目錄下的 `provider_endpoints_support.json`。**

此檔案追蹤每個 LiteLLM provider 支援哪些端點，並用於生成文件。

**必要步驟：**
1. 對於 release notes 中新增的每個 provider，在 `provider_endpoints_support.json` 中加入對應條目
2. 對於新增的每個端點類型，更新 schema 註解並將端點加入相關的 provider

**Provider 條目格式：**
```json
"provider_slug": {
  "display_name": "Provider Name (`provider_slug`)",
  "url": "https://docs.litellm.ai/docs/providers/provider_slug",
  "endpoints": {
    "chat_completions": true,
    "messages": true,
    "responses": true,
    "embeddings": false,
    "image_generations": false,
    "audio_transcriptions": false,
    "audio_speech": false,
    "moderations": false,
    "batches": false,
    "rerank": false,
    "a2a": true
  }
}
```

**可用端點類型：**
- `chat_completions` - `/chat/completions` 端點
- `messages` - `/messages` 端點 (Anthropic 格式)
- `responses` - `/responses` 端點 (OpenAI/Anthropic 統一格式)
- `embeddings` - `/embeddings` 端點
- `image_generations` - `/image/generations` 端點
- `audio_transcriptions` - `/audio/transcriptions` 端點
- `audio_speech` - `/audio/speech` 端點
- `moderations` - `/moderations` 端點
- `batches` - `/batches` 端點
- `rerank` - `/rerank` 端點
- `ocr` - `/ocr` 端點
- `search` - `/search` 端點
- `vector_stores` - `/vector_stores` 端點
- `a2a` - `/a2a/{agent}/message/send` 端點 (A2A 協定)

**檢查清單：**
- [ ] Release notes 中的所有新 provider 已加入 `provider_endpoints_support.json`
- [ ] 端點支援旗標準確反映供應商能力
- [ ] 文件 URL 指向正確的供應商文件頁面

## 範例指令工作流

```bash
# 1. 取得模型變更
git diff <commit> HEAD -- model_prices_and_context_window.json

# 2. 分析 PR 清單進行分類
# 3. 按照模板建立 release notes
# 4. 連結至適當文件
# 5. 審查是否缺少文件需求
```

## 輸出要求

- 嚴格遵循參考資料的 markdown 結構
- 包含所有 PR 連結與貢獻者
- 提供準確的模型價格表格
- 連結至相關文件
- 使用警告標示重大變更
- 包含部署指令
- 以完整的 changelog 連結結尾

此流程確保生成一致且全面的 release notes，幫助使用者了解變更並順利升級。
