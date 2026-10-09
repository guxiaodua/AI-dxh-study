import os
import json
from pathlib import Path
from typing import Sequence

from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi

def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")

class FileChatMessageHistory(BaseChatMessageHistory):
    # 【修复1】__int__ → __init__
    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        # 【修复2】逗号错误 self,session_id → self.session_id 增加json后缀
        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json")

        # 创建文件夹
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # 文件不存在新建空文件
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    # 【修复3】参数名 message → messages
    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(msg) for msg in all_messages]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=2)

    # 【修复4】提升缩进层级，不要嵌套在add_messages里面；名称必须是messages
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                message_data = json.load(f)
            # 【修复5】字典列表 转换成消息对象
            return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)

