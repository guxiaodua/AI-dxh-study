'''
知识库
'''
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    '''检查传入的字符串是否已处理过'''
    if not os.path.exists(config.md5_path):
        # 文件不存在，以w打开，可以自动创建文件
        open(config.md5_path, 'w', encoding='utf-8').close
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False
        


def save_md5(md5_str: str):
    '''将传入的md5字符串，记录到文件中保存'''
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    '''将传入的字符串转换为md5字符串'''
    # 将字符串转换为bytes字节数组
    str_byte = input_str.encode(encoding=encoding)
    # 创建md5对象
    md5_obj = hashlib.md5()
    md5_obj.update(str_byte)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name, # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory, # 数据库本地存储文件夹
        )      # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 分隔后的文本段最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段之间字符重叠数量
            separators=config.separators, # 自然段落划分的符号
            length_function=len, # 使用python自带的len函数做长度统计的依据
        )     # 文本分割器对象

    def upload_by_str(self, data: str, filename):
        '''将传入的字符串，进行向量化，存入向量数据库中'''
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return '[跳过]内容已经存在知识库中'

        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "小咸鱼"
        }

        self.chroma.add_texts( # 内容就加载到向量数据库中了
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    res = service.upload_by_str("大咸鱼11", "test_file")
    print(res)