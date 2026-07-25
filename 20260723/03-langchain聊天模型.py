from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

# 获取模型对象
model = ChatTongyi(model="qwen3-max")

# 准备消息列表
message = [
    SystemMessage(content="你是一个情种"),
    HumanMessage(content="请写一副对联"),
    AIMessage(content="一二三四五，上山打老虎"),
    HumanMessage(content="请按你上一个回复的格式，再写一首对联")
]

# 调用stream流式执行
res = model.stream(input=message)

# 循环输出结果
for chunk in res:
    print(chunk.content,end="",flush=True)