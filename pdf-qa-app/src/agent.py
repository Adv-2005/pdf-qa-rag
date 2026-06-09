from langchain_ollama import ChatOllama

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import ChatPromptTemplate

from src.tools import (
    pdf_search,
    rag_answer,
    web_search
)


def build_agent():

    llm = ChatOllama(
        model="gemma4:e4b",
        temperature=0
    )

    tools = [
        pdf_search,
        rag_answer,
        web_search
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a helpful assistant.

Choose the correct tool:

1. rag_answer
   - Use when the user asks a question about the uploaded PDF.
   - Return a final answer.

2. pdf_search
   - Use when the user wants raw text, excerpts,
     retrieved chunks, references, or relevant passages
     from the PDF.

3. web_search
   - Use when the question requires current information
     or information not available in the uploaded PDF.

Always use a tool whenever appropriate.
Do not make up answers.
"""
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    )

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor