import os
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi

# ========== 1. 定义工具 get_weather ==========
@tool(description="获取指定城市明天的天气，当用户询问天气时调用。")
def get_weather(city: str) -> str:
    """
    获取指定城市明天的天气，当用户询问天气时调用。
    Args:
        city: 城市名称，例如：深圳、北京
    """
    # 这里是模拟天气接口，你可以替换成真实天气API
    return f"{city}明天：多云，气温24~30℃，微风。"

# ========== 2. 创建智能体Agent ==========
agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),    # 智能体的大脑LLM
    tools=[get_weather],                   # 向智能体提供工具列表
    system_prompt="你是一个聊天助手，可以回答用户问题。",
)

# ========== 3. 调用agent ==========
res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "明天深圳的天气如何？"},
        ]
    }
)

# ========== 4. 遍历打印消息 ==========
for msg in res["messages"]:
    print(type(msg).__name__, msg.content)
