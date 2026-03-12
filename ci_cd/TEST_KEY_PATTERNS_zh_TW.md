# 測試金鑰模式標準

LiteLLM 程式碼庫中測試/模擬金鑰和憑證的標準模式，以避免觸發金鑰偵測。

## GitGuardian 的運作方式

GitGuardian 使用 **機器學習和熵分析**，而不僅僅是模式比對：
- **低熵** 值（如 `sk-1234`、`postgres`）會被自動忽略
- **高熵** 值（看起來真實的金鑰）會觸發偵測
- **上下文感知** 偵測能理解程式碼語法，如 `os.environ["KEY"]`

## 推薦的測試金鑰模式

### 選項 1：低熵值（最簡單）
這些不會觸發 GitGuardian 的機器學習偵測器：

```python
api_key = "sk-1234"
api_key = "sk-12345"
database_password = "postgres"
token = "test123"
```

### 選項 2：帶有測試前綴的高熵
如果您需要具有高熵且看起來真實的測試金鑰，請使用以下前綴：

```python
api_key = "sk-test-abc123def456ghi789..."  # OpenAI 風格測試金鑰
api_key = "sk-mock-1234567890abcdef1234..."  # 模擬金鑰
api_key = "sk-fake-xyz789uvw456rst123..."  # 偽造金鑰
token = "test-api-key-with-high-entropy"
```

## 設定的忽略模式

這些模式已在 `.gitguardian.yaml` 中設定，用於高熵測試金鑰：
- `sk-test-*` - OpenAI 風格測試金鑰
- `sk-mock-*` - 模擬 API 金鑰
- `sk-fake-*` - 偽造 API 金鑰
- `test-api-key` - 通用測試權杖
