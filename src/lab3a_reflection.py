from langgraph.graph import StateGraph, START, END
from states import SummaryState, SummaryStateInput, SummaryStateOutput
from IPython.display import Image, display

  

def generate_search_query(state: SummaryState):
    """Generate an effective search query for the research topic."""
    ...
    
    return {"search_query": 'query'}

def perform_web_search(state: SummaryState):
    """Perform a web search using the Tavily API."""
    ...
    
    return {"sources_gathered": 'search_results'}


def summarize_search_results(state: SummaryState):
    """Summarize the information from search results."""
    ...
    
    return {"running_summary": 'summary'}

def identify_knowledge_gaps(state: SummaryState):
    """Identify knowledge gaps and generate a follow-up query."""
    ...
    
    return {"search_query": 'follow_up_query'}

# Step 5: Finalize the summary
def finalize_summary(state: SummaryState):
    ...
    return {"running_summary": 'final_summary'}

# Conditional function that decides whether to continue research or finalize summary
def route_research(state: SummaryState):
    if state.research_loop_count <= 2:
        return "web_research"
    else:
        return "finalize_summary" 

# Set up the graph
def setup_graph():
    # Add nodes and edges
    builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput)
    builder.add_node("generate_query", generate_search_query)
    builder.add_node("web_research", perform_web_search)
    builder.add_node("summarize_sources", summarize_search_results)
    builder.add_node("reflect_on_summary", identify_knowledge_gaps)
    builder.add_node("finalize_summary", finalize_summary)
    
    # Add edges
    builder.add_edge(START, "generate_query")
    builder.add_edge("generate_query", "web_research")
    builder.add_edge("web_research", "summarize_sources")
    builder.add_edge("summarize_sources", "reflect_on_summary")
    builder.add_conditional_edges("reflect_on_summary", route_research)
    builder.add_edge("finalize_summary", END)
    
    return builder.compile()  


if __name__ == "__main__":

    graph = setup_graph()
    display(Image(graph.get_graph().draw_mermaid_png()))    
