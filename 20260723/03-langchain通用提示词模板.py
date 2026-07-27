from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

pt = PromptTemplate.from_template(
    "我刚生了个{gender}，我姓{name},请取一个好听的名字，简单回答。"
)

model = Tongyi(model="qwen-max")

# 直接调用模型注入
# pt_text = pt.format(name="代",gender="女儿")
# res = model.invoke(input=pt_text)
# print(res)

chain = pt | model
res = chain.invoke(input={"name":"代","gender":"女儿"})
print(res)