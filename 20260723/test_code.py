from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="dummy"  # ollama本地不需要真实key，必须填一个占位，不能空
)

messages = [{"role": "user", "content": "吃麻辣火锅怎么样"}]
completion = client.chat.completions.create(
    model="qwen3.5:9b-q4_K_M",
    messages=messages,
    stream=True,
    # 关键：传给ollama的显存控制参数
    extra_body={
        "options": {
            "num_ctx": 2048,
            "num_gpu": 24
        }
    }
)

print("\n" + "=" * 20 + "完整回复" + "=" * 20)
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)