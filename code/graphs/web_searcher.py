from langgraph.constants import START, END
from langchain_core.messages import get_buffer_string
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from instructions import pi_instructions
from code.env_setting import llm, tavily_search
from code.states.states import PrivateInvestigatorState

def search_web(state: PrivateInvestigatorState):
    """ Retrieve docs from web search """

    # Search
    query = state['search_query']
    search_docs = tavily_search.invoke(query)
    # Format
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}



def generate_finding(state: PrivateInvestigatorState):
    """ Node to see if the sentence is in any of Tavily search results """

    # Get state
    messages = state["messages"]
    context = state["context"]
    query = state["search_query"]
    # Answer question
    system_message = pi_instructions.format(context=context, query=query)
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)

    # Name the message as coming from the expert
    answer.name = "PI"

    # Append it to state
    return {"messages": [answer]}


def save_findings(state: PrivateInvestigatorState):
    """ Save Findings """

    # Get messages
    messages = state["messages"]

    # Convert interview to a string
    findings = get_buffer_string(messages)

    # Save to interviews key
    return {"findings": [findings]}


# Add nodes and edges
pi_builder = StateGraph(PrivateInvestigatorState)
pi_builder.add_node("search_web", search_web)
pi_builder.add_node("check_if_copied", generate_finding)
pi_builder.add_node("save_findings", save_findings)

# Flow
pi_builder.add_edge(START, "search_web")
pi_builder.add_edge("search_web", "check_if_copied")
pi_builder.add_edge("check_if_copied", "save_findings")
pi_builder.add_edge("save_findings", END)

# Interview
memory = MemorySaver()
pi_graph = pi_builder.compile(checkpointer=memory).with_config(run_name="PI run")
