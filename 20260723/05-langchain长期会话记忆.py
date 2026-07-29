import os,json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from typing import Sequence
from langchain_core.messages import BaseMessage


# message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict: [字典、字典...] -> [消息、消息...]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件，所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self,session_id)

        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, message: Sequence[BaseMessage]) -> None:
        # Swquence序列 类似list,tuple
        all_messages = list(self.messages)  # 已有的消息列表
        all_messages.extend(message)        # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 二进制文件
        # 为了方便，可以将BaseMessage消息转为字典
        # message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)
        
        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

        @property
        def message(self) -> list[BaseMessage]:
            # 当前文件内：list[字典]
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    message_data = json.load(f)
            except FileNotFoundError:
                return []

        def clear(self) -> None:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)



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

# 相当于一个map
def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

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

    # res = c_chain.invoke({"input": "一个共有多少个动物"}, session_cfg)
    # print("第三次执行: ", res)
