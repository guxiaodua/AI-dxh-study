'''
基于Streamlit完成WEB网页上传服务
安装：
pip install streamlit

运行：
streamlit run 文件名

当web页面元素发生变化，则代码重新执行一遍
提供了字典 st.session_state 不会刷新
'''
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title('RAG知识库更新服务')
# file_uploader
uploader_file = st.file_uploader(
    "请上传文件",
    type=['txt','csv'],
    accept_multiple_files=False, # 只接受一个文件上传
)

# session_satate就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件信息
    name = uploader_file.name
    type = uploader_file.type
    size = uploader_file.size / 1024 # KB

    st.subheader(f"文件名:{name}")
    st.write(f"格式:{type} | 大小:{size:.2f}KB")

    # get_value - bytes - decode('utf-8')
    text = uploader_file.getvalue().decode('utf-8')
    st.write(text)

    with st.spinner("载入知识库中……"): # 在spinner内的代码执行过程中，会有一个转圈的动画
        time.sleep(1)
        res = st.session_state["service"].upload_by_str(text, name)
        st.write(res)