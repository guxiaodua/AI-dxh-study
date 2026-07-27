from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate

'''
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable ...
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> ...
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> ...
'''

template = PromptTemplate.from_template("我的邻居是：{name},喜欢{hobby}")

res = template.format(name="小明", hobby="小小强")
print(res, type(res))

res2 = template.invoke({"name":"二明","hobby":"三狗"})
print(res2, type(res2))