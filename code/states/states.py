import operator
from typing import Annotated, TypedDict, List

from langgraph.graph import MessagesState


# web searcher state
class PrivateInvestigatorState(MessagesState):
    context: Annotated[list, operator.add]  # Source docs
    findings: Annotated[list, operator.add]  # Final key we duplicate in outer state for Send() API
    search_query: str

# PI_team_leader state
class ResearchGraphState(TypedDict):
    source_text: str # original text to look for cheaters from.
    queries: List[str] # queries to search for
    findings: Annotated[list, operator.add] # Send() API key
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Final report