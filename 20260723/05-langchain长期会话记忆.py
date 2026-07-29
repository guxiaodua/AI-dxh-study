import os,json
from langchain_core.messages import message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory

# message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict: [字典、字典...] -> [消息、消息...]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __int__(self, session_id, storage_path):
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