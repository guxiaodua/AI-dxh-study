from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

model = ChatOllama(
    model="qwen3.5:9b-q4_K_M",
    base_url="http://127.0.0.1:11434",
    temperature=0.7,
    timeout=300,
    model_kwargs={
        "num_ctx": 2048,
        "num_gpu": 18
    }
)

# ✅ 标准消息对象写法
messages = [
    SystemMessage(content="你是一个情种"),
    HumanMessage(content="请写一副对联"),
    AIMessage(content="上上下下吃，上山打老虎"),
    HumanMessage(content="模仿上一个，写一首对联"),
]

res = model.stream(messages)

for chunk in res:
    print(chunk.content, end="", flush=True)
print("\n")