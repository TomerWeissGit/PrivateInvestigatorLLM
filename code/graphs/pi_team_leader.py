from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import Send
from langchain_core.messages import HumanMessage, SystemMessage
from code.graphs.instructions import text_splitter_instructions, report_writer_instructions, conclusion_instructions
from code.env_setting import llm
from code.states.states import ResearchGraphState
from code.graphs.web_searcher import pi_builder
from langgraph.graph import StateGraph
from langgraph.constants import START, END

def split_to_queries(state: ResearchGraphState):
    text = state['source_text']
    system_message = text_splitter_instructions.format(text=text)
    split_sentences = llm.invoke([SystemMessage(content=system_message)] + [
        HumanMessage(content=f"split me the sentences based on the provided text")])
    return {'queries': split_sentences.content.split('split_here')}


def map_search(state: ResearchGraphState):
    """ This is the "map" step where we run each interview sub-graph using Send API """

    return [Send("search_cheaters", {"search_query": query, "messages": [HumanMessage(content=f"")]}) for query in
            state["queries"]]




def write_report(state: ResearchGraphState):
    # Full set of findings
    findings = state["findings"]

    # Concat all findings together
    formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])

    # Summarize the findings into a final report
    system_message = report_writer_instructions.format(context=formatted_str_findings)
    report = llm.invoke(
        [SystemMessage(content=system_message)] + [HumanMessage(content=f"Write a report based upon these memos.")])
    return {"content": report.content}


def write_conclusion(state: ResearchGraphState):
    # Full set of findings
    findings = state["findings"]

    # Concat all findings together
    formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])

    # Summarize the findings into a final report

    instructions = conclusion_instructions.format(formatted_str_findings=formatted_str_findings)
    conclusion = llm.invoke([instructions] + [HumanMessage(content=f"Write the report conclusion")])
    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
    """ The is the "reduce" step where we gather all the findings, combine them, and reflect on them to write the conclusion """
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
builder = StateGraph(ResearchGraphState)
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
