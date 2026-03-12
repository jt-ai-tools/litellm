# 貢獻至 LiteLLM

感謝您對貢獻 LiteLLM 的興趣！我們歡迎各種形式的貢獻 —— 從 Bug 修復和文件改進到新功能與整合。

## **提交 PR 前的檢查清單**

以下是提交至 LiteLLM 的任何 PR 的核心要求：

- [ ] **簽署貢獻者授權協議 (CLA)** - [詳情請見](#貢獻者授權協議-cla)
- [ ] **保持範圍獨立** - 您的更改一次應僅解決 1 個特定的問題

#### Proxy (後端) PR

- [ ] **加入測試** - 加入至少 1 個測試是硬性要求 - [詳情請見](#加入測試)
- [ ] **確保您的 PR 通過所有檢查**：
  - [ ] [單元測試](#執行單元測試) - `make test-unit`
  - [ ] [Linting / 格式化](#執行-linting-與格式化檢查) - `make lint`

#### UI PR

- [ ] **確保 UI 構建成功** - `npm run build`
- [ ] **確保所有 UI 單元測試通過** - `npm run test`
- [ ] **為新組件或邏輯加入測試** - 如果您要加入新組件或新邏輯，請加入相應的測試

## **貢獻者授權協議 (CLA)**

在為 LiteLLM 貢獻程式碼之前，您必須簽署我們的 [貢獻者授權協議 (CLA)](https://cla-assistant.io/BerriAI/litellm)。這是將所有貢獻合併到主倉庫的法律要求。

**重要：** 我們強烈建議在開始貢獻工作之前審閱並簽署 CLA，以避免 PR 過程中的任何延遲。

## 快速入門

### 1. 設定您的本地開發環境

```bash
# 在 GitHub 上 Fork 倉庫（點擊 https://github.com/BerriAI/litellm 上的 Fork 按鈕）
# 然後將您的 Fork 克隆到本地
git clone https://github.com/YOUR_USERNAME/litellm.git
cd litellm

# 為您的功能建立一個新分支
git checkout -b your-feature-branch

# 安裝開發依賴
make install-dev

# 驗證您的設定是否正常運作
make help
```

就這樣！您的本地開發環境已準備就緒。

### 2. 開發工作流

以下是進行更改的推薦工作流：

```bash
# 對程式碼進行更改
# ...

# 格式化您的程式碼（自動修復格式問題）
make format

# 執行所有 Lint 檢查（與 CI 完全一致）
make lint

# 執行單元測試以確保沒有損壞任何內容
make test-unit

# 提交您的更改
git add .
git commit -m "您的描述性提交訊息"

# 推播並建立 PR
git push origin your-feature-branch
```

## 加入測試

**加入至少 1 個測試是所有 PR 的硬性要求。**

### 在哪裡加入測試

將您的測試加入到 [`tests/test_litellm/` 目錄](https://github.com/BerriAI/litellm/tree/main/tests/test_litellm)。

- 此目錄鏡像了 `litellm/` 目錄的結構
- **僅加入 Mock 測試** - 此目錄中不允許進行真實的 LLM API 呼叫
- 對於使用真實 API 的整合測試，請使用相應的測試目錄

### 檔案命名規範

`tests/test_litellm/` 目錄遵循與 `litellm/` 相同的結構：

- `litellm/proxy/caching_routes.py` → `tests/test_litellm/proxy/test_caching_routes.py`
- `litellm/utils.py` → `tests/test_litellm/test_utils.py`

### 測試範例

```python
import pytest
from litellm import completion

def test_your_feature():
    """使用描述性的 docstring 測試您的功能。"""
    # Arrange (安排)
    messages = [{"role": "user", "content": "Hello"}]
    
    # Act (行動)
    # 使用 Mock 回應，而非真實的 API 呼叫
    
    # Assert (斷言)
    assert expected_result == actual_result
```

## 執行測試與檢查

### 執行單元測試

執行所有單元測試（使用並行執行以提高速度）：

```bash
make test-unit
```

執行特定的測試檔案：
```bash
poetry run pytest tests/test_litellm/test_your_file.py -v
```

### 執行 Linting 與格式化檢查

執行所有 Lint 檢查（與 CI 完全一致）：

```bash
make lint
```

個別的 Lint 指令：
```bash
make format-check       # 檢查 Black 格式
make lint-ruff          # 執行 Ruff Lint
make lint-mypy          # 執行 MyPy 型別檢查
make check-circular-imports    # 檢查循環導入
make check-import-safety       # 檢查導入安全性
```

套用格式化（自動修復問題）：
```bash
make format
```

### CI 相容性

為了確保您的更改能通過 CI，請在本地執行完全相同的檢查：

```bash
# 這將執行與 GitHub 工作流相同的檢查
make lint
make test-unit
```

為了獲得精確的 CI 相容性（固定 OpenAI 版本，如 CI）：
```bash
make install-dev-ci     # 安裝精確的 CI 依賴
```

## 可用的 Make 指令

執行 `make help` 查看所有可用指令：

```bash
make help                       # 顯示所有可用指令
make install-dev               # 安裝開發依賴
make install-proxy-dev         # 安裝 Proxy 開發依賴
make install-test-deps         # 安裝測試依賴（用於執行測試）
make format                    # 套用 Black 程式碼格式化
make format-check              # 檢查 Black 格式（與 CI 一致）
make lint                      # 執行所有 Lint 檢查
make test-unit                 # 執行單元測試
make test-integration          # 執行整合測試
make test-unit-helm            # 執行 Helm 單元測試
```

## 程式碼品質標準

LiteLLM 遵循 [Google Python 風格指南](https://google.github.io/styleguide/pyguide.html)。

我們的自動化品質檢查包括：
- **Black** 用於一致的程式碼格式化
- **Ruff** 用於 Lint 與程式碼品質
- **MyPy** 用於靜態型別檢查
- **循環導入檢測**
- **導入安全性驗證**

所有檢查必須通過，您的 PR 才能被合併。

## 常見問題與解決方案

### 1. Linting 失敗

如果 `make lint` 失敗：

1. **格式問題**：執行 `make format` 自動修復
2. **Ruff 問題**：檢查輸出並手動修復
3. **MyPy 問題**：加入正確的型別提示 (Type Hints)
4. **循環導入**：重構導入依賴關係
5. **導入安全性**：修復任何未受保護的導入

### 2. 測試失敗

如果 `make test-unit` 失敗：

1. 檢查您是否破壞了現有功能
2. 為您的新程式碼加入測試
3. 確保測試使用 Mock，而非真實的 API 呼叫
4. 檢查測試檔案命名規範

### 3. 常見開發提示

- **使用型別提示**：MyPy 要求正確的型別標註
- **撰寫描述性的提交訊息**：幫助評審者理解您的更改
- **保持 PR 專注**：每個 PR 僅包含一個功能/修復
- **測試邊緣案例**：不要只測試正常路徑
- **更新文件**：如果您更改了 API，請更新文件

## 在本地構建與執行

### LiteLLM Proxy Server

要在本地執行 Proxy 伺服器：

```bash
# 安裝 Proxy 依賴
make install-proxy-dev

# 啟動 Proxy 伺服器
poetry run litellm --config your_config.yaml
```

### Docker 開發

如果您想自己構建 Docker 映像：

```bash
# 使用非 root 的 Dockerfile 進行構建
docker build -f docker/Dockerfile.non_root -t litellm_dev .

# 使用您的配置運行
docker run \
    -v $(pwd)/proxy_config.yaml:/app/config.yaml \
    -e LITELLM_MASTER_KEY="sk-1234" \
    -p 4000:4000 \
    litellm_dev \
    --config /app/config.yaml --detailed_debug
```

## UI 開發

### 1. 設定您的本地 UI 開發環境

```bash
# 克隆倉庫（如果您還沒有這麼做）
git clone https://github.com/YOUR_USERNAME/litellm.git
cd litellm

# 導航至 UI 儀表板目錄
cd ui/litellm-dashboard

# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev
```

### 2. 加入 UI 測試

如果您要加入 **新組件** 或 **新邏輯**，您必須加入相應的測試。

### 3. 執行 UI 單元測試

```bash
npm run test
```

### 4. 構建 UI

在提交 PR 前確保 UI 構建成功：

```bash
npm run build
```

## 提交您的 PR

1. **推播您的分支**：`git push origin your-feature-branch`
2. **建立 PR**：前往 GitHub 並建立 Pull Request
3. **填寫 PR 模板**：提供更改的清晰描述
4. **等待評審**：維護者將進行評審並提供反饋
5. **處理反饋**：根據要求進行更改並推播更新
6. **合併**：一旦獲得批准，您的 PR 將被合併！

## 獲取幫助

如果您需要幫助：

- 💬 [加入我們的 Discord](https://discord.gg/wuPM9dRgDw)
- 💬 [加入我們的 Slack](https://www.litellm.ai/support)
- 📧 電子郵件聯絡我們：ishaan@berri.ai / krrish@berri.ai
- 🐛 [建立 Issue](https://github.com/BerriAI/litellm/issues/new)

## 可以貢獻什麼

正在尋找靈感嗎？查看：

- 🐛 [適合初學者的 Issue (Good first issues)](https://github.com/BerriAI/litellm/labels/good%20first%20issue)
- 🚀 [功能請求](https://github.com/BerriAI/litellm/labels/enhancement)
- 📚 文件改進
- 🧪 測試覆蓋率改進
- 🔌 新的 LLM 供應商整合

感謝您對 LiteLLM 的貢獻！🚀
