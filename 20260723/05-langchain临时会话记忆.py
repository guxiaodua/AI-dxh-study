from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template(
#     "你需要根据历史会话回答用户问题，对话历史：{chat_history}，用户提问：{input}，请回答"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回答用户问题，对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}"),
    ]
)

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print('='*10, full_prompt.to_string(), '='*10)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

store = {} # key就是session，value就是InMemoryChatMessageHistory类对象

# 相当于一个map
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

c_chain = RunnableWithMessageHistory(
    base_chain,     # 被增强的原有chain
    get_history,    # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",             # 表示用户输入在模板中的提问占位符
    history_messages_key="chat_history",    # 表示用户输入在模板中的历史占位符
)

if __name__ == '__main__':
    session_cfg = {
        "configurable": {
            "session_id": "user_001",
        }
    }

    res = c_chain.invoke({"input": "小明有一只狗"}, session_cfg)
    print("第一次执行: ", res)

    res = c_chain.invoke({"input": "小红三个小鸡"}, session_cfg)
    print("第二次执行: ", res)

    res = c_chain.invoke({"input": "一个共有多少个动物"}, session_cfg)
    print("第三次执行: ", res)
