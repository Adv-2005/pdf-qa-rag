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
        model="qwen2.5:3b",
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
You are assisting users with an uploaded PDF.

IMPORTANT:

Assume that user questions refer to the uploaded PDF unless the user clearly asks for information outside the PDF.

Tool Selection Rules:

1. rag_answer
   - Use for answering questions about the uploaded PDF.
   - This should be your default choice.

2. pdf_search
   - Use when the user asks for exact text, passages, excerpts, references, or retrieved chunks from the PDF.

3. web_search
   - Use ONLY when:
     * the user explicitly asks for current/latest information
     * the question is clearly unrelated to the uploaded PDF
     * the PDF tools cannot answer

Always prefer PDF tools over web_search when a PDF is available.
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