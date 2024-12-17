# Private Investigator: A Search Tool for Scientific Paper Originality
A RAG model built using LangChain &amp; Tavily used for finding Copied parts in text

## Introduction

Private Investigator is a powerful tool designed to assess the originality of scientific papers. By leveraging LangChain, OpenAI's GPT models, and the Tavily Search API,
this tool efficiently retrieves and analyzes relevant data to detect whether a paper contains copied content or demonstrates originality.

With Private Investigator, researchers, reviewers, and academics can ensure scientific integrity by identifying potential duplications and enhancing the transparency of scientific publications.

The main idea behind this project is to utilize tavily search while demonstrating how to use concepts such as multi-agent, map-reduce and LangGraph.
## Setup

### Python version

To get the most out of this course, please ensure you're using Python 3.11 or later. 
This version is required for optimal compatibility with LangGraph. If you're on an older version, 
upgrading will ensure everything runs smoothly.

```
python3 --version
```
for mac users make sure you have brew installed and then you can upgrade your python version using the following on your cmd:
```
brew upgrade python3
```

### Clone repo
```
git clone [https://github.com/TomerWeissGit/PrivateInvestigatorLLM.git]
$ cd PrivateInvestigatorLLM
```

### Create an environment and install dependencies
#### Mac/Linux/WSL
```
$ python3.xy -m venv pi_env
$ source pi_env/bin/activate
$ pip install -r requirements.txt
```
#### Windows Powershell
```
PS> python3 -m venv pi_env
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> pi_env\scripts\activate
PS> pip install -r requirements.txt
```

### Running notebooks
If you don't have Jupyter set up, follow installation instructions [here](https://jupyter.org/install).
```
$ jupyter notebook
```

### Setting up env variables
* rename the `.env_example` file in the project folder to `.env`
* insert the API keys that you created instead of the "xxxxx".
use a `.env` file with `python-dotenv` library (already in code).


#### Set OpenAI API key
* If you don't have an OpenAI API key, you can sign up [here](https://openai.com/index/openai-api/).
*  Set `OPENAI_API_KEY` in your `.env` file.

#### Sign up and Set LangSmith API
* Sign up for LangSmith [here](https://smith.langchain.com/), find out more about LangSmith
* and how to use it within your workflow [here](https://www.langchain.com/langsmith), and relevant library [docs](https://docs.smith.langchain.com/)!
*  Set `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2="true"` and `LANGCHAIN_PROJECT="yourprojectname"` in your `.env` file.

#### Set up Tavily API for web search

* Tavily Search API is a search engine optimized for LLMs and RAG, aimed at efficient, 
quick, and persistent search results. 
* You can sign up for an API key [here](https://tavily.com/). 
It's easy to sign up and offers a very generous free tier. 

* Set `TAVILY_API_KEY` in your `.env` file.

# Structure:
The structure of the PI LangGraph is quite simple and easy to understand, it is build from a main graph which utilizes a Tavily based subgraph in a map-reduce algorithm. Both Graphs operates different agents in order to make sure the task is achived in the 
right way and to seperate between different smaller tasks.

## Sub-Graph - Web Searcher
The web searcher sub graph contains 3 nodes:
* "search_web" - a node which uses Tavily and a given query to search on the web, this node is very important because it saves the content of the search which will be examined in the next node-this is our context.
* "check_if_copied" - this node is our private investigator, it checkes if the given query has a 1:1 match with some of the context given by Tavily.
* "save_findings" - this node is only responsible for saving the findings from our privare investigator.
  ![graph1](https://github.com/user-attachments/assets/67b4bf75-6ce0-4839-abd9-6ab0f4cc3f43)
