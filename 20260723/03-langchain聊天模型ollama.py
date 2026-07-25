from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 获取模型对象，增加显存控制参数
model = ChatOllama(
    model="qwen3.5:9b-q4_K_M",
    base_url="http://127.0.0.1:11434",
    temperature=0.7,
    timeout=300,  # 超时5分钟，长文本推理避免直接断开
    extra_headers={},
    # 传给Ollama底层参数，防止AMD DirectML显存溢出终止
    options={
        "num_ctx": 2048,
        "num_gpu": 24
    }
)

# 准备消息列表
messages = [
    # SystemMessage(content="你是一个情种"),
    HumanMessage(content="请写一副对联"),
]

# 调用stream流式执行
res = model.stream(input=messages)

# 循环输出结果
for chunk in res:
    print(chunk.content, end="", flush=True)
print("\n")