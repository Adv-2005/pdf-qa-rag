from langchain_core.tools import tool
import os

from dotenv import load_dotenv
from serpapi import GoogleSearch
from requests.exceptions import RequestException


load_dotenv()

retriever = None


def set_retriever(r):
    global retriever
    retriever = r


@tool
def pdf_search(query: str) -> str:
    """
    Search the uploaded PDF for relevant information.
    """

    if retriever is None:
        return "No PDF loaded."

    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        page = doc.metadata.get("page", "Unknown")

        results.append(
            f"Page {page}\n{doc.page_content}"
        )

    return "\n\n".join(results)

#rag answer tool

qa_chain = None


def set_qa_chain(chain):
    global qa_chain
    qa_chain = chain


@tool
def rag_answer(query: str) -> str:
    """
    Answer questions using the uploaded PDF.
    Uses retrieval augmented generation (RAG).
    """

    if qa_chain is None:
        return "No PDF has been loaded."

    response = qa_chain.invoke(
        {"input": query}
    )

    return response.get(
        "answer",
        str(response)
    )

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information.

    Use this tool when information is not available
    in the uploaded PDF or requires up-to-date data.
    """

    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        return "Web search is unavailable because SERP_API_KEY is not set."

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
    except RequestException as exc:
        return (
            "Web search failed because the network request could not be completed. "
            f"Details: {exc}"
        )
    except Exception as exc:
        return f"Web search failed unexpectedly: {exc}"

    organic_results = results.get(
        "organic_results",
        []
    )

    formatted = []

    for item in organic_results[:5]:

        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")

        formatted.append(
            f"Title: {title}\n"
            f"Snippet: {snippet}\n"
            f"Link: {link}"
        )

    return "\n\n".join(formatted)
