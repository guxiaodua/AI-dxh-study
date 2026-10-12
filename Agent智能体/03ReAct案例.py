# ========== 导入 import ==========
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from langchain.agents import create_agent

# ========== 定义工具 @tool ==========
@tool(description="获取身高，传入人名，返回字符串信息。每轮只能单独调用这一个工具。")
def get_height(name: str) -> str:
    return f"{name}的身高是175厘米"


@tool(description="获取体重，传入人名，返回字符串信息。每轮只能单独调用这一个工具。")
def get_weight(name: str) -> str:
    return f"{name}的体重是68公斤"


# ========== 创建Agent ==========
agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_height, get_weight],
    system_prompt=(
        "你是一个智能助手，使用 ReAct（Reason + Act）方式回答问题。"
        "规则：每轮仅调用一个工具，禁止一次并行调用多个工具。"
        "需要多个信息时，先思考再调用其中一个工具，观察结果后，下一轮再调用另一个工具。"
        "请告知我思考过程，让我知道你为什么调用某个工具。"
    ),
)

# ========== 流式遍历输出 ==========
for chunk in agent.stream(
    input={"messages": [{"role": "user", "content": "小咸鱼的身高和体重分别是多少？"}]},
    stream_mode="values",
):
    latest_message = chunk["messages"][-1]

    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content)

    try:
        if latest_message.tool_calls:
            print(f"工具调用: {[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass
