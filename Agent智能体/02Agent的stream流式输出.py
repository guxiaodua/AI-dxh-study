# ========== 导入 import ==========
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from langchain.agents import create_agent

# ========== 定义工具 @tool ==========
@tool(description="获取股价，传入股票名称，返回字符串信息")
def get_price(name: str) -> str:
    return f"股票{name}的价格是20美元"


@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name: str) -> str:
    return f"股票{name}，是一家A股上市公司，专注于显卡收割。"


# ========== 创建Agent ==========
agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_price, get_info],
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具"
)

# ========== 流式遍历输出 ==========
for chunk in agent.stream(
    input={"messages": [{"role": "user", "content": "英伟达股价多少，并介绍一下"}]},
    stream_mode="values"
):
    latest_message = chunk['messages'][-1]

    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content)

    try:
        if latest_message.tool_calls:
            print(f"工具调用: {[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError as e:
        pass
