from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage

parser = StrOutputParser()
model = ChatTongyi(model="qwen3-max")
prompt = PromptTemplate.from_template(
    "我刚生了个{gender}，我姓{name},请取一个好听的名字，简单回答。"
)

chain = prompt | model | parser | model
res: AIMessage = chain.invoke({"gender":"女儿","name":"代"})
print(res.content)