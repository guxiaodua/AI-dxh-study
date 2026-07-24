from openai import OpenAI
# 1、获取client对象，OpenAI
client = OpenAI(
    base_url='https://ws-d0ndnclzj3aanvm0.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)
# 2、调用模型
response = client.chat.completions.create(
    model='qwen3.7-plus',
    messages=[
        {"role":"system","content":"你是一个python专家，并且不会说废话简单回答"},
        {"role":"assistant","content":"你好，我是python专家，人狠话不多，请问需要什么帮助吗？"},
        {"role":"user","content":"输出1-99数字，使用python代码"},
    ],
    stream=True, # 开启流式输出功能
)
# 3、处理结果
# print(response.choices[0].message.content)
for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end="&", # 每一段之间以&分隔
        flush=True # 立刻刷新缓冲区
    )