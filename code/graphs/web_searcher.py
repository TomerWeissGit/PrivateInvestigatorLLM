from langchain_core.messages import SystemMessage
from langchain_core.messages import get_buffer_string
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from code.env_setting import llm, tavily_search
from code.instructions.instructions import web_searcher_instructions
from code.states.states import PrivateInvestigatorState


class WebSearcherGraph:
    def __init__(self):
        """
        This class represents the web searcher graph, it is a simple graph used to answer if a sentence is copied from
        the internet or not.
        The Graph is build out of 3 nodes:
        * search_web - responsible for looking for the sentence on the web using Tavily search.
        * check_if_copied - responsible for generate a proper response, whether the sentence is copied or not.
        * save_findings - saves the findings in the state 'findings' list.
        """
        # Initialize the StateGraph
        self.builder = StateGraph(PrivateInvestigatorState)

        # Add nodes
        self.builder.add_node("search_web", self.search_web)
        self.builder.add_node("check_if_copied", self.generate_finding)
        self.builder.add_node("save_findings", self.save_findings)

        # Define the flow
        self.builder.add_edge(START, "search_web")
        self.builder.add_edge("search_web", "check_if_copied")
        self.builder.add_edge("check_if_copied", "save_findings")
        self.builder.add_edge("save_findings", END)

        # Compile the graph
        self.memory = MemorySaver()
        self.graph = self.builder.compile(checkpointer=self.memory)

    @staticmethod
    def search_web(state: PrivateInvestigatorState):
        """
        Retrieve docs from web search using the pre-defined Tavily search tool
        :param state: a state containing 'search_query' which is the query to search for.
        :return: a formatted search docs in a list, which appends to the state context.
        """
        query = state["search_query"]
        search_docs = tavily_search.invoke(query)

        # Format the search results
        formatted_search_docs = "\n\n---\n\n".join(
            [f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>' for doc in search_docs]
        )

        return {"context": [formatted_search_docs]}

    @staticmethod
    def generate_finding(state: PrivateInvestigatorState):
        """
        Node to see if the sentence is in any of Tavily search results
        :param state: The privateInvestigatorState which contains messages, context and search_query.
        :return: the PI answer, in a list, which appends to the other messages in the state.        """
        messages = state["messages"]
        context = state["context"]
        query = state["search_query"]

        # Generate the finding
        system_message = web_searcher_instructions.format(context=context, query=query)
        answer = llm.invoke([SystemMessage(content=system_message)] + messages)

        # Name the message as coming from the "PI"
        answer.name = "PI"

        return {"messages": [answer]}

    @staticmethod
    def save_findings(state: PrivateInvestigatorState):
        """
        Save findings into state
        :param state: The privateInvestigatorState which contains findings.
        :return: a list containing the findings, which appends to other findings found in the state
        """
        messages = state["messages"]
        findings = get_buffer_string(messages)
        return {"findings": [findings]}


