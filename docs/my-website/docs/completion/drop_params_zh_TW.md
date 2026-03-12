import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 捨棄不支援的參數 (Drop Unsupported Params)

由您的 LLM 供應商捨棄不支援的 OpenAI 參數。

## 預設行為 (Default Behavior)

**預設情況下，LiteLLM 會拋出異常 (exception)**，如果您向模型發送它不支援的參數。

例如，如果您向不支援 `temperature` 參數的模型發送 `temperature=0.2`，LiteLLM 將拋出異常。

**當設置 `drop_params=True` 時**，LiteLLM 將捨棄不支援的參數而不是拋出異常。這允許您的程式碼在不同的供應商之間無縫運行，而無需為每個供應商自定義參數。

## 快速上手 (Quick Start) 

```python 
import litellm 
import os 

# 設置金鑰 
os.environ["COHERE_API_KEY"] = "co-.."

litellm.drop_params = True # 👈 關鍵更改

response = litellm.completion(
                model="command-r",
                messages=[{"role": "user", "content": "Hey, how's it going?"}],
                response_format={"key": "value"},
            )
```


LiteLLM 按供應商 + 模型映射所有支援的 openai 參數（例如，Bedrock 上的 Anthropic 支援函數呼叫，但 Titan 不支援）。

參見 `litellm.get_supported_openai_params("command-r")` [**程式碼**](https://github.com/BerriAI/litellm/blob/main/litellm/utils.py#L3584)

如果供應商/模型不支援特定參數，您可以將其捨棄。

## OpenAI Proxy 用法

```yaml
litellm_settings:
    drop_params: true
```

## 在 `completion(..)` 中傳遞 drop_params

僅在呼叫特定模型時捨棄參數 (drop_params)

<Tabs>
<TabItem value="sdk" label="SDK">

```python 
import litellm 
import os 

# 設置金鑰 
os.environ["COHERE_API_KEY"] = "co-.."

response = litellm.completion(
                model="command-r",
                messages=[{"role": "user", "content": "Hey, how's it going?"}],
                response_format={"key": "value"},
                drop_params=True
            )
```
</TabItem>
<TabItem value="proxy" label="PROXY">

```yaml
- litellm_params:
    api_base: my-base
    model: openai/my-model
    drop_params: true # 👈 關鍵更改
  model_name: my-model
```
</TabItem>
</Tabs>

## 指定要捨棄的參數 (Specify params to drop)

要在呼叫供應商時捨棄特定參數（例如 vllm 的 'logit_bias'）

使用 `additional_drop_params`

<Tabs>
<TabItem value="sdk" label="SDK">

```python
import litellm 
import os 

# 設置金鑰 
os.environ["COHERE_API_KEY"] = "co-.."

response = litellm.completion(
                model="command-r",
                messages=[{"role": "user", "content": "Hey, how's it going?"}],
                response_format={"key": "value"},
                additional_drop_params=["response_format"]
            )
```
</TabItem>
<TabItem value="proxy" label="PROXY">

```yaml
- litellm_params:
    api_base: my-base
    model: openai/my-model
    additional_drop_params: ["response_format"] # 👈 關鍵更改
  model_name: my-model
```
</TabItem>
</Tabs>

**additional_drop_params**: 列表或 null - 是您在呼叫模型時想要捨棄的 openai 參數列表。

### 巢狀欄位移除 (Nested Field Removal)

使用類似 JSONPath 的表示法捨棄複雜對象中的巢狀欄位：

<Tabs>
<TabItem value="sdk" label="SDK">

```python
import litellm

response = litellm.completion(
    model="bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=[{"role": "user", "content": "Hello"}],
    tools=[{
        "name": "search",
        "description": "Search files",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
        "input_examples": [{"query": "test"}]  # 將被移除
    }],
    additional_drop_params=["tools[*].input_examples"]  # 從所有工具中移除
)
```

</TabItem>
<TabItem value="proxy" label="PROXY">

```yaml
model_list:
  - model_name: my-bedrock-model
    litellm_params:
      model: bedrock/us.anthropic.claude-sonnet-4-5-20250929-v1:0
      additional_drop_params: ["tools[*].input_examples"]  # 從所有工具中移除
```

</TabItem>
</Tabs>

**支援的語法：**
- `field` - 頂層欄位
- `parent.child` - 巢狀物件欄位
- `array[*]` - 所有陣列元素
- `array[0]` - 特定陣列索引
- `tools[*].input_examples` - 所有陣列元素中的欄位
- `tools[0].metadata.field` - 特定索引 + 巢狀欄位

**範例使用案例：**
- 從工具定義中移除 `input_examples` (Claude Code + AWS Bedrock)
- 從巢狀結構中捨棄供應商特定欄位
- 在發送到 LLM 之前清理巢狀參數

## 在請求中指定允許的 openai 參數

告訴 litellm 在請求中允許特定的 openai 參數。如果您收到 `litellm.UnsupportedParamsError` 並想允許某個參數，請使用此功能。LiteLLM 將按原樣將參數傳遞給模型。



<Tabs>
<TabItem label="LiteLLM Python SDK" value="Python">

在此範例中，我們傳遞 `allowed_openai_params=["tools"]` 以允許 `tools` 參數。

```python showLineNumbers title="向 LiteLLM Python SDK 傳遞 allowed_openai_params"
await litellm.acompletion(
    model="azure/o_series/<my-deployment-name>",
    api_key="xxxxx",
    api_base=api_base,
    messages=[{"role": "user", "content": "Hello! return a json object"}],
    tools=[{"type": "function", "function": {"name": "get_current_time", "description": "Get the current time in a given location.", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The city name, e.g. San Francisco"}}, "required": ["location"]}}}]
    allowed_openai_params=["tools"],
)
```
</TabItem>
<TabItem value="proxy" label="LiteLLM Proxy">

使用 litellm proxy 時，您可以通過兩種方式傳遞 `allowed_openai_params`：

1. 在請求中動態傳遞 `allowed_openai_params`
2. 在 config.yaml 檔案中為特定模型設置 `allowed_openai_params`

#### 在請求中動態傳遞 allowed_openai_params
在此範例中，我們傳遞 `allowed_openai_params=["tools"]` 以允許發送到代理上設置的模型的請求使用 `tools` 參數。

```python showLineNumbers title="在請求中動態傳遞 allowed_openai_params"
import openai
from openai import AsyncAzureOpenAI

import openai
client = openai.OpenAI(
    api_key="anything",
    base_url="http://0.0.0.0:4000"
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [
        {
            "role": "user",
            "content": "this is a test request, write a short poem"
        }
    ],
    extra_body={ 
        "allowed_openai_params": ["tools"]
    }
)
```

#### 在 config.yaml 上設置 allowed_openai_params

您也可以在 config.yaml 檔案中為特定模型設置 `allowed_openai_params`。這意味著所有發送到此部署的請求都允許傳入 `tools` 參數。

```yaml showLineNumbers title="在 config.yaml 上設置 allowed_openai_params"
model_list:
  - model_name: azure-o1-preview
    litellm_params:
      model: azure/o_series/<my-deployment-name>
      api_key: xxxxx
      api_base: https://openai-prod-test.openai.azure.com/openai/deployments/o1/chat/completions?api-version=2025-01-01-preview
      allowed_openai_params: ["tools"]
```
</TabItem>
</Tabs>
