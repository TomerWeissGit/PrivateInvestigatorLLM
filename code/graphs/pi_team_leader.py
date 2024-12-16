from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.constants import Send
from langgraph.graph import StateGraph

from code.env_setting import llm
from code.graphs.web_searcher import pi_builder
from code.instructions.instructions import text_splitter_instructions, report_writer_instructions, \
    conclusion_instructions
from code.states.states import TeamLeaderState


def split_to_queries(state: TeamLeaderState):
    """
    Split the source text into sub-queries by splitting into different sentences.
    It uses the text splitter instructions in order to split the text in a pre-defined way.
    :param state: a ResearchGraphState object containing the source text
    :return: a list of queries
    """
    text = state['source_text']
    system_message = text_splitter_instructions.format(text=text)
    split_sentences = llm.invoke([SystemMessage(content=system_message)] + [
        HumanMessage(content=f"split me the sentences based on the provided text")])
    return {'queries': split_sentences.content.split('split_here')}


def map_search(state: TeamLeaderState):
    """
    Map the search queries to the search_cheaters node, which will run the search for each query.
    This is the "map" step where we run each interview sub-graph using Send API which uses parallelization.
    :param state: a ResearchGraphState object containing the queries.
    :return: a list of Send objects to run the search_cheaters node for each query."""

    return [Send("search_cheaters", {"search_query": query, "messages": [HumanMessage(content=f"")]}) for query in
            state["queries"]]


def write_report(state: TeamLeaderState):
    """
    Write a report based on the findings from the search_cheaters node.
    The report created is based on the report_writer_instructions and the findings from the search_cheaters node.
    :param state: a ResearchGraphState object containing the findings.
    :return: a report content.
    """
    # Full set of findings
    findings = state["findings"]

    # Concat all findings together
    formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])

    # Summarize the findings into a final report
    system_message = report_writer_instructions.format(context=formatted_str_findings)
    report = llm.invoke(
        [SystemMessage(content=system_message)] + [HumanMessage(content=f"Write a report based upon these memos.")])
    return {"content": report.content}


def write_conclusion(state: TeamLeaderState):
    """
    Write a conclusion based on the findings from the search_cheaters node.
     The conclusion is based on the conclusion_instructions and the findings from the search_cheaters node.
    :param state: a ResearchGraphState object containing the findings.
    :return: a conclusion content.
    """
    # Full set of findings
    findings = state["findings"]

    # Concat all findings together
    formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])

    # Summarize the findings into a final report

    instructions = conclusion_instructions.format(formatted_str_findings=formatted_str_findings)
    conclusion = llm.invoke([instructions] + [HumanMessage(content=f"Write the report conclusion")])
    return {"conclusion": conclusion.content}


def finalize_report(state: TeamLeaderState):
    """
    Finalize the report by combining the content and conclusion into a final report.
    :param state: a ResearchGraphState object containing the content and conclusion.
    :return: a final report content.
    """
    # Save full final report
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except ValueError:
            sources = None
    else:
        sources = None

    final_report = "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report}


# Add nodes and edges
builder = StateGraph(TeamLeaderState)
builder.add_node("split_to_queries", split_to_queries)
builder.add_node("search_cheaters", pi_builder.compile())
builder.add_node("write_report", write_report)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

# Logic
builder.add_edge(START, "split_to_queries")
builder.add_conditional_edges("split_to_queries", map_search, ['search_cheaters'])
builder.add_edge("search_cheaters", "write_report")
builder.add_edge("search_cheaters", "write_conclusion")
builder.add_edge(["write_conclusion", "write_report"], "finalize_report")
builder.add_edge("finalize_report", END)

# Compile
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
