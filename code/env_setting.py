import getpass
import os

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

load_dotenv()

# setting up the environment variables if they are not set already
def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

_set_env("OPENAI_API_KEY")
_set_env("TAVILY_API_KEY")
_set_env("LANGCHAIN_API_KEY")
_set_env("LANGCHAIN_TRACING_V2")
_set_env("LANGCHAIN_PROJECT")

llm = ChatOpenAI(model="gpt-4o",temperature=0)
tavily_search = TavilySearchResults(max_results=3)
