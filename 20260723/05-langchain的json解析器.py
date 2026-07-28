from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage

str_parser = StrOutputParser()
json_parser = JsonOutputParser()
model = ChatTongyi(model="qwen3-max")
first_prompt = PromptTemplate.from_template(
    "我刚生了个{gender}，我姓{name},请取一个好听的名字，请返回json格式，key为name，value为你取的名字，请严格按照要求"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请分析名字的含义"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser
res: AIMessage = chain.invoke({"gender":"女儿","name":"代"})
print(res)