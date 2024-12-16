import operator
import os, getpass
from typing import List, Annotated, TypedDict
from IPython.display import Markdown
from langgraph.constants import Send
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from IPython.display import Image, display
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import get_buffer_string
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")
_set_env("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "PI"

llm = ChatOpenAI(model="gpt-4o",temperature=0)
tavily_search = TavilySearchResults(max_results=3)

if __name__ == "__main__":
    pass