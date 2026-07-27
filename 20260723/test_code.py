import ollama

messages = [
    {"role":"system","content":"你是一个情种，擅长写对联"},
    {"role":"user","content":"写一副对联"}
]

resp = ollama.chat(
    model="qwen3.5:9b-q4_K_M",
    messages=messages,
    stream=True,
    options={
        "num_ctx":2048,
        "num_gpu":18
    }
)

for chunk in resp:
    print(chunk["message"]["content"],end="",flush=True)