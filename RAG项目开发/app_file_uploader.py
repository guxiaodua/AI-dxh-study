'''
基于Streamlit完成WEB网页上传服务
pip install streamlit
'''
import streamlit as st

# 添加网页标题
st.title('RAG知识库更新服务')
# file_uploader
uploader_file = st.file_uploader(
    "请上传文件",
    type=['txt','csv'],
    accept_multiple_files=False, # 只接受一个文件上传
)

if uploader_file is not None:
    # 提取文件信息
    name = uploader_file.name
    type = uploader_file.type
    size = uploader_file.size / 1024 #KB

    st.subheader(f"文件名:{name}")
    st.write(f"格式:{type} | 大小:{size:.2f}KB")

    # get_value - bytes - decode('utf-8')
    text = uploader_file.getvalue().decode('utf-8')
    st.write(text)