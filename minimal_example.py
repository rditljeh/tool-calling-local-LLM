from typing import List

from langchain.messages import AIMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama
import webbrowser


@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def perform_google_search(query: str) -> None:
    """Take the users question, modify it to improve results, and open a web browser to perform a google search"""
    query = query.replace(" ", "+")
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return

llm = ChatOllama(
    model="deepseek-r1:8b",
    validate_model_on_init=True,
    temperature=0,
).bind_tools([add, multiply])

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)

if isinstance(result, AIMessage) and result.tool_calls:
    print(result.tool_calls)