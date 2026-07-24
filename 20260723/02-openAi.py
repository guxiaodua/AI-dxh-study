from openai import OpenAI
# 1、获取client对象，OpenAI
client = OpenAI(
    base_url='https://ws-d0ndnclzj3aanvm0.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)
# 2、调用模型
response = client.chat.completions.create(
    model='qwen3.7-plus',
    messages=[
        {"role":"system","content":"你是一个AI助手，回答很简洁"},
        {"role":"user","content":"小明有三个饼干"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小红有8个饼干"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"总共有多少个饼干？"},
    ],
    stream=True, # 开启流式输出功能
)
# 3、处理结果
# print(response.choices[0].message.content)
# for chunk in response:
#     print(
#         chunk.choices[0].delta.content,
#         end=" ", # 每一段之间以空格分隔
#         flush=True # 立刻刷新缓冲区
#     )

for chunk in response:
    # 关键判断：空choices直接跳过
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    # content不为None才打印
    if delta.content is not None:
        print(
            delta.content,
            end=" ",
            flush=True
        )
print("\n流式输出结束")