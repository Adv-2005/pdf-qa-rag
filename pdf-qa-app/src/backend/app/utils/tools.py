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



#rag answer tool

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
