import os
import json
import dotenv
from typing import Dict, List, Any, Tuple
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from langgraph.graph import StateGraph, START, END

from stream_llm_response import stream_thinking_and_answer, display_panel, strip_thinking_tokens
from prompts import query_writer_instructions, summarizer_instructions, get_current_date, reflection_instructions
from states import SummaryState, SummaryStateInput, SummaryStateOutput
from formatting import deduplicate_and_format_sources, format_sources

# Load environment variables
dotenv.load_dotenv()

# Initialize console and clients
console = Console()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
model_name = os.getenv("AZURE_DEEPSEEK_DEPLOYMENT")
key = os.getenv("AZURE_AI_API_KEY")

# Set up the AI model
model = AzureAIChatCompletionsModel(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    model_name=model_name,  
)
  

def generate_search_query(state: SummaryState):
    """Generate an effective search query for the research topic."""
    console.print("[bold blue]Generating optimal search query...[/]")

    # Format the prompt
    current_date = get_current_date()

    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=state.research_topic
    )
    
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content=f"Generate a query for web search. The research topic is: {state.research_topic}")
    ]
    
    # Stream the model's thinking process
    console.print("\n[bold]Query Generation Process:[/]\n")
    response_stream = model.invoke(messages)
    thoughts, query = strip_thinking_tokens(response_stream)
    
    display_panel(f"**Search Query**: {query}", "🔍 Generated Search Query and updated state.search_query", "green")
    
    return {"search_query": query}

def perform_web_search(state: SummaryState):
    """Perform a web search using the Tavily API."""
    console.print("\n[bold blue]Performing web search...[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Searching the web...", total=None)
        search_results = tavily_client.search(query=state.search_query, max_results=3)
    
    # Display search result snippets
    console.print("\n[bold]Search Results:[/]")
    for i, result in enumerate(search_results["results"], 1):
        display_panel(
            f"**Title**: {result['title']}\n\n**Snippet**: {result['content']}\n\n**URL**: {result['url']}",
            f"Result {i}",
            "blue"
        )
    display_panel(
            f"updated state.web_research_results and state.research_loop_count",
            "green"
        )
    
    search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
    
    return {"sources_gathered": [format_sources(search_results)], "research_loop_count": state.research_loop_count + 1, "web_research_results": [search_str]}


def summarize_search_results(state: SummaryState):
    """Summarize the information from search results."""
    console.print("\n[bold blue]Synthesizing information from search results...[/]")

    # Existing summary
    existing_summary = state.running_summary

    # Most recent web research
    most_recent_web_research = state.web_research_results[-1]
    
    # Build the human message
    if existing_summary:
        human_message_content = (
            f"<Existing Summary> \n {existing_summary} \n </Existing Summary>\n\n"
            f"<New Context> \n {most_recent_web_research} \n </New Context>"
            f"Update the Existing Summary with the New Context on this topic: \n <User Input> \n {state.research_topic} \n </User Input>\n\n"
        )
    else:
        human_message_content = (
            f"<Context> \n {most_recent_web_research} \n </Context>"
            f"Create a Summary using the Context on this topic: \n <User Input> \n {state.research_topic} \n </User Input>\n\n"
        )
    
    messages = [
        SystemMessage(content=summarizer_instructions),
        HumanMessage(content=human_message_content)
    ]
    
    # Stream the model's thinking process for summarization
    console.print("\n[bold]Summarization Process:[/]\n")
    response_stream = model.invoke(messages)
    thoughts, summary = strip_thinking_tokens(response_stream)
    
    display_panel(summary, "📝 Research Summary created and updated state.running_summary", "green")
    
    return {"running_summary": summary}

def identify_knowledge_gaps(state: SummaryState):
    """Identify knowledge gaps and generate a follow-up query."""
    console.print("\n[bold blue]Identifying knowledge gaps...[/]")
    
    messages = [
        SystemMessage(content=reflection_instructions.format(research_topic=state.research_topic)),
        HumanMessage(content=f"Reflect on our existing knowledge: \n === \n {state.running_summary}, \n === \n And now identify a knowledge gap and generate a follow-up web search query:")
    ]
    
    # Stream the model's thinking process for knowledge gap identification
    console.print("\n[bold]Knowledge Gap Analysis Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, json_str = stream_thinking_and_answer(response_stream, "🔍 Reflection Thinking")
    
    # Try to parse the JSON response
    try:
        reflection = json.loads(json_str)
        knowledge_gap = reflection.get("knowledge_gap", "No specific knowledge gap identified.")
        follow_up_query = reflection.get("follow_up_query", f"More information about {state.research_topic}")
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        knowledge_gap = "Unable to parse the identified knowledge gap."
        follow_up_query = f"More information about {state.research_topic}"
    
    display_panel(
        f"**Knowledge Gap**: {knowledge_gap}\n\n**Follow-up Query**: {follow_up_query}",
        "🔍 Knowledge Gap Analysis done and updated state.search_query and state.knowledge_gap",
        "yellow"
    )
    
    return {"search_query": follow_up_query, "knowledge_gap": knowledge_gap}

# Step 5: Finalize the summary
def finalize_summary(state: SummaryState):
    console.print("\n[bold]===== Final Research Report =====[/]\n")

    # Format the final summary
    final_summary = f"## Summary\n{state.running_summary}\n\n### Sources:\n"
    for source in state.sources_gathered:
        final_summary += f"{source}\n"

    
    display_panel(final_summary, "📊 Complete Research Report and updated state.running_summary", "purple")
    return {"running_summary": final_summary}

# Conditional function that decides whether to continue research or finalize summary
def route_research(state: SummaryState):
    if state.research_loop_count <= 2:
        display_panel("web_research", "📊 Doing more research", "orange")
        return "web_research"
    else:
        display_panel("finalize_summary", "📊 Finalizing the summary", "orange")
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

def main():
    """Main function to run the web research demo."""
    console.print("[bold blue]===== Deep Research: Web Research Integration Demo =====\n")
    
    console.print("[yellow]This demo shows how AI models can be enhanced with web search capabilities.")
    console.print("[yellow]You'll see multiple research cycles with query generation, web search, and synthesis.")
    console.print("[yellow]The AI's thinking will be streamed live in real-time at each stage.\n")
    
    while True:
        research_topic = Prompt.ask("[bold green]Enter a research topic[/] (or 'exit' to quit)")
        
        if research_topic.lower() in ("exit", "quit", "q"):
            console.print("\n[bold blue]Thank you for using the Deep Research web integration demo.[/]")
            break
        
        # Conduct research with two iterations
        # Set up the graph
        graph = setup_graph()

        def stream_graph_updates():
            for event in graph.stream({"research_topic": research_topic}):
                # Extract the node name and state from the event
                node_name = next(iter(event.keys()), None)

                print(node_name)

        stream_graph_updates()
        
        console.print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()
