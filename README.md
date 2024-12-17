# Private Investigator: A Search Tool for Scientific Paper Originality
A Retrieval-Augmented Generation (RAG) model built using **LangChain** and **Tavily Search API** to identify copied parts of text in scientific papers.

## Introduction
**Private Investigator** is a powerful tool designed to evaluate the originality of scientific papers. By integrating **LangChain**, **OpenAI's GPT models**, and the **Tavily Search API**, it efficiently retrieves and analyzes relevant data to detect content duplication or ensure originality.

The tool demonstrates advanced concepts such as **multi-agent systems**, **map-reduce workflows**, and **LangGraph** to provide accurate and structured results. Researchers, reviewers, and academics can leverage this tool to enhance scientific integrity by identifying potential duplications and improving transparency in publications.

## Setup

### Python Version
Ensure you are using **Python 3.11 or later** for compatibility with LangGraph. To check your current Python version:
```bash
python3 --version
```
For Mac users, ensure you have `brew` installed, and upgrade Python using:
```bash
brew upgrade python3
```

### Clone the Repository
```bash
git clone https://github.com/TomerWeissGit/PrivateInvestigatorLLM.git
cd PrivateInvestigatorLLM
```

### Create an Environment and Install Dependencies
#### Mac/Linux/WSL
```bash
python3.xy -m venv pi_env
source pi_env/bin/activate
pip install -r requirements.txt
```
#### Windows Powershell
```powershell
python3.xy -m venv pi_env
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
pi_env\scripts\activate
pip install -r requirements.txt
```

### Running Notebooks
If you don’t have Jupyter installed, follow the [official installation guide](https://jupyter.org/install).
```bash
jupyter notebook
```

### Setting Up Environment Variables
1. Rename the `.env_example` file in the project folder to `.env`.
2. Replace placeholder values (`xxxxx`) with your API keys.

#### Set OpenAI API Key
- Obtain an OpenAI API key [here](https://openai.com/index/openai-api/).
- Add the following line to your `.env` file:
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```

#### Set LangSmith API
- Sign up for LangSmith [here](https://smith.langchain.com/).
- Configure your `.env` file:
  ```
  LANGCHAIN_API_KEY=your_langsmith_api_key
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_PROJECT=your_project_name
  ```

#### Set Up Tavily API for Web Search
- Obtain a Tavily API key [here](https://tavily.com/).
- Add the following to your `.env` file:
  ```
  TAVILY_API_KEY=your_tavily_api_key
  ```

## Project Structure
The **Private Investigator** is built using a **main graph** and a **sub-graph**, demonstrating the power of LangGraph in executing workflows efficiently.

### Sub-Graph: Web Searcher
The **Web Searcher** sub-graph performs three primary tasks:
1. **`search_web`**: Uses Tavily to search the web with a given query and retrieves contextual content.
2. **`check_if_copied`**: Analyzes the retrieved content to identify 1:1 matches (potential duplications). The findings include links and proof of copied text.
3. **`save_findings`**: Saves the results for downstream processing.

![Web Searcher Graph](https://github.com/user-attachments/assets/67b4bf75-6ce0-4839-abd9-6ab0f4cc3f43)

### Main Graph: PI Team Leader
The **PI Team Leader** graph orchestrates the entire workflow, breaking the problem into smaller tasks and consolidating results. Key components include:

1. **`split_to_queries`**: Splits the input text into individual sentences using an LLM.
2. **`map_search`** -> **`search_cheaters`**: Maps each sentence to the **Web Searcher sub-graph**, executing searches in parallel to identify copied content.
3. **`write_conclusion`** and **`write_report`**: Generates a concise report and verdict based on findings.
4. **`finalize_report`**: Merges the report and conclusion into a polished final output presented to the user.

![Main Graph](https://github.com/user-attachments/assets/3c33a86d-7b24-41ff-83d2-cc710ef1ccc5)

## User-Friendly Notebooks
For a more hands-on experience, a user-friendly notebook is included. It runs the code with clear explanations, visualizations, and less object-oriented structure for easier understanding.

---
