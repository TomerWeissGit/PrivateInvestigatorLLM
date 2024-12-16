from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END, Send
from langgraph.graph import StateGraph
from code.env_setting import llm
from code.graphs.web_searcher import WebSearcherGraph
from code.instructions.instructions import text_splitter_instructions, report_writer_instructions, conclusion_instructions
from code.states.states import TeamLeaderState


class TeamLeaderGraph:
    def __init__(self):
        """
        Initialize the TeamLeaderGraph class.
        The Graph is build out of 5 parts:
        * splits_to_queries - responsible for splitting the source text into sub-queries.
        * search_cheaters - activates the subgraph responsible for searching for cheaters - WebSearcherGraph.
        * write_report - writes a report based on the findings.
        * write_conclusion - writes a conclusion based on the findings.
        * finalize_report - finalizes the report by combining the content and conclusion.
        """
        # Initialize the state graph
        self.builder = StateGraph(TeamLeaderState)

        # Add nodes to the graph
        self.builder.add_node("split_to_queries", self.split_to_queries)
        self.builder.add_node("search_cheaters", WebSearcherGraph().builder.compile())
        self.builder.add_node("write_report", self.write_report)
        self.builder.add_node("write_conclusion", self.write_conclusion)
        self.builder.add_node("finalize_report", self.finalize_report)

        # Define the edges of the graph
        self.builder.add_edge(START, "split_to_queries")
        self.builder.add_conditional_edges("split_to_queries", self.map_search, ["search_cheaters"])
        self.builder.add_edge("search_cheaters", "write_report")
        self.builder.add_edge("search_cheaters", "write_conclusion")
        self.builder.add_edge(["write_conclusion", "write_report"], "finalize_report")
        self.builder.add_edge("finalize_report", END)

        # Compile the graph
        self.memory = MemorySaver()
        self.graph = self.builder.compile(checkpointer=self.memory)

    @staticmethod
    def split_to_queries(state: TeamLeaderState):
        """
        Split the source text into sub-queries by splitting into different sentences.
        It uses the text splitter instructions in order to split the text in a pre-defined way.
        :param state: a ResearchGraphState object containing the source text
        :return: a list of queries
        """
        text = state["source_text"]
        system_message = text_splitter_instructions.format(text=text)
        split_sentences = llm.invoke(
            [SystemMessage(content=system_message)] +
            [HumanMessage(content="Split the sentences based on the provided text.")]
        )
        return {"queries": split_sentences.content.split("split_here")}

    @staticmethod
    def map_search(state: TeamLeaderState):
        """
        Map the search queries to the search_cheaters node, which will run the search for each query.
        This is the "map" step where we run each interview sub-graph using Send API which uses parallelization.
        :param state: a ResearchGraphState object containing the queries.
        :return: a list of Send objects to run the search_cheaters node for each query."""
        return [
            Send("search_cheaters", {
                "search_query": query,
                "messages": [HumanMessage(content="")]
            }) for query in state["queries"]
        ]
    @staticmethod
    def write_report(state: TeamLeaderState):
        """
        Write a report based on the findings from the search_cheaters node.
        The report created is based on the report_writer_instructions and the findings from the search_cheaters node.
        :param state: a ResearchGraphState object containing the findings.
        :return: a report content.
        """
        findings = state["findings"]
        formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])
        system_message = report_writer_instructions.format(context=formatted_str_findings)
        report = llm.invoke(
            [SystemMessage(content=system_message)] +
            [HumanMessage(content="Write a report based upon these memos.")]
        )
        return {"content": report.content}

    @staticmethod
    def write_conclusion(state: TeamLeaderState):
        """
        Write a conclusion based on the findings from the search_cheaters node.
         The conclusion is based on the conclusion_instructions and the findings from the search_cheaters node.
        :param state: a ResearchGraphState object containing the findings.
        :return: a conclusion content.
        """
        findings = state["findings"]
        formatted_str_findings = "\n\n".join([f"{finding}" for finding in findings])
        instructions = conclusion_instructions.format(formatted_str_findings=formatted_str_findings)
        conclusion = llm.invoke(
            [SystemMessage(content=instructions)] +
            [HumanMessage(content="Write the report conclusion.")]
        )
        return {"conclusion": conclusion.content}

    @staticmethod
    def finalize_report(state: TeamLeaderState):
        """
        Finalize the report by combining the content and conclusion into a final report.
        :param state: a ResearchGraphState object containing the content and conclusion.
        :return: a final report content.
        """

        content = state["content"]
        if content.startswith("## Insights"):
            content = content.strip("## Insights")
        sources = None
        if "## Sources" in content:
            try:
                content, sources = content.split("\n## Sources\n")
            except ValueError:
                pass
        final_report = f"\n\n---\n\n{content}\n\n---\n\n{state['conclusion']}"
        if sources:
            final_report += f"\n\n## Sources\n{sources}"
        return {"final_report": final_report}


