import os, getpass
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
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
