from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_templete = ChatPromptTemplate.from_messages(
    [
        ("system", "你是个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human", "再来一首唐诗"),
    ]
)

history_data = [
    ("human", "你来写一首唐诗"),
    ("ai", "床前明月光，疑似地上霜，举头望明月，低头思故乡"),
    ("human", "好诗，再来一个"),
    ("ai", "锄禾日当午，汗滴禾下锄，谁知盘中餐，粒粒皆辛苦"),
]

promp_text = chat_prompt_templete.invoke({"history": history_data}).to_string()

model = ChatTongyi(model="qwen3-max")

res = model.invoke(promp_text)

print(res.content, type(res))