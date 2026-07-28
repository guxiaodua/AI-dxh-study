from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

str_parser = StrOutputParser()
# json_parser = JsonOutputParser()
model = ChatTongyi(model="qwen3-max")
first_prompt = PromptTemplate.from_template(
    "我刚生了个{gender}，我姓{name},请取一个好听的名字，只告诉我名字，不要其他信息"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请分析名字的含义"
)

my_func = RunnableLambda(lambda ai_msg: {"name", ai_msg.content})

chain = first_prompt | model | my_func | second_prompt | model
# res = chain.stream({"gender":"男孩","name":"代"})

for chunk in chain.stream({"gender":"男孩","name":"代"}):
    print(chunk.content,end="",flush=True)