'''
知识库
'''
import os
import config_data as config
import hashlib

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
        self.chroma = None      # 向量存储的实例 Chroma向量库对象
        self.spliter = None     # 文本分割器对象

    def upload_by_str(self, data, filename):
        '''将传入的字符串，进行向量化，存入向量数据库中'''
        pass

if __name__ == '__main__':
    save_md5('5f5bdf0ba2b705701d096e369084453b')
    print(check_md5('5f5bdf0ba2b705701d096e369084453b'))