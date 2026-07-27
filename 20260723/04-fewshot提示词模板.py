from langchain_core.prompts import FewShotPromptTemplate

FewShotPromptTemplate(
    example_prompt=None,    # 示例数据的模板
    examples=None,          # 示例的数据（用来注入动态数据的），list内套字典
    prefix=None,            # 示例之前的提示词
    suffix=None,            # 示例之后的提示词
    input_variables=[]      # 声明在前缀或后缀中所需要注入的变量名
)