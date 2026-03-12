# 函數呼叫 (Function Calling) 

## 檢查模型是否支援函數呼叫 (Function Calling)

使用 `litellm.supports_function_calling(model="")` -> 如果模型支援函數呼叫則返回 `True`，否則返回 `False`

```python
assert litellm.supports_function_calling(model="gpt-3.5-turbo") == True
assert litellm.supports_function_calling(model="azure/gpt-4-1106-preview") == True
assert litellm.supports_function_calling(model="palm/chat-bison") == False
assert litellm.supports_function_calling(model="xai/grok-2-latest") == True
assert litellm.supports_function_calling(model="ollama/llama2") == False
```


## 檢查模型是否支援並行函數呼叫 (Parallel Function Calling)

使用 `litellm.supports_parallel_function_calling(model="")` -> 如果模型支援並行函數呼叫則返回 `True`，否則返回 `False`

```python
assert litellm.supports_parallel_function_calling(model="gpt-4-turbo-preview") == True
assert litellm.supports_parallel_function_calling(model="gpt-4") == False
```
## 並行函數呼叫 (Parallel Function Calling)
並行函數呼叫是模型同時執行多個函數呼叫的能力，允許這些函數呼叫的效果和結果被並行解析。

## 快速上手 - gpt-3.5-turbo-1106 (Quick Start)
<a target="_blank" href="https://colab.research.google.com/github/BerriAI/litellm/blob/main/cookbook/Parallel_function_calling.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

在此範例中，我們定義了一個單一函數 `get_current_weather`。

- 步驟 1：向模型發送 `get_current_weather` 以及用戶的問題
- 步驟 2：解析模型回應的輸出 - 使用模型提供的參數執行 `get_current_weather`
- 步驟 3：向模型發送執行 `get_current_weather` 函數的輸出


### 完整程式碼 - 使用 `gpt-3.5-turbo-1106` 進行並行函數呼叫

```python
import litellm
import json
# 設置 openai api key
import os
os.environ['OPENAI_API_KEY'] = "" # litellm 從 .env 讀取 OPENAI_API_KEY 並發送請求

# 硬編碼返回相同天氣的範例虛擬函數
# 在生產環境中，這可能是您的後端 API 或外部 API
def get_current_weather(location, unit="fahrenheit"):
    """獲取給定位置的當前天氣"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def test_parallel_function_call():
    try:
        # 步驟 1：將對話和可用函數發送給模型
        messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a given location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ]
        response = litellm.completion(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto",  # auto 是預設值，但我們這裡明確指定
        )
        print("\nFirst LLM Response:\n", response)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        print("\nLength of tool calls", len(tool_calls))

        # 步驟 2：檢查模型是否想要呼叫函數
        if tool_calls:
            # 步驟 3：呼叫函數
            # 注意：JSON 回應可能並不總是有效的；請確保處理錯誤
            available_functions = {
                "get_current_weather": get_current_weather,
            }  # 此範例中只有一個函數，但您可以有多個
            messages.append(response_message)  # 用助手的回覆擴展對話

            # 步驟 4：將每個函數呼叫的資訊和函數回應發送給模型
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # 用函數回應擴展對話
            second_response = litellm.completion(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # 從模型獲取新的回應，此時它可以看到函數回應
            print("\nSecond LLM response:\n", second_response)
            return second_response
    except Exception as e:
      print(f"Error occurred: {e}")

test_parallel_function_call()
```

### 說明 - 並行函數呼叫
以下是對上述使用 `gpt-3.5-turbo-1106` 進行並行函數呼叫的程式碼片段的說明。
### 步驟 1：litellm.completion() 設置 `tools` 為 `get_current_weather`
```python
import litellm
import json
# 設置 openai api key
import os
os.environ['OPENAI_API_KEY'] = "" # litellm 從 .env 讀取 OPENAI_API_KEY 並發送請求
# 硬編碼返回相同天氣的範例虛擬函數
# 在生產環境中，這可能是您的後端 API 或外部 API
def get_current_weather(location, unit="fahrenheit"):
    """獲取給定位置的當前天氣"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    }
]

response = litellm.completion(
    model="gpt-3.5-turbo-1106",
    messages=messages,
    tools=tools,
    tool_choice="auto",  # auto 是預設值
)
```
