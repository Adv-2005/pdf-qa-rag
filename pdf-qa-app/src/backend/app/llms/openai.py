from langchain_openai import ChatOpenAI

answer_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

grader_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
