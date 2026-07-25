# langchain_community
from langchain_ollama import OllamaLLM
# 不要用qwen3.7-plus, qwen3.7-plus属于多模态模型，qwen-max是大语言模型
model = OllamaLLM(model="qwen3.5:9b-q4_K_M")
# 调用invoke向模型提问
res = model.invoke(input="你是谁，你可以做什么？")

print(res)