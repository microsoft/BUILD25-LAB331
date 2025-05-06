import os
import dotenv
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

from stream_llm_response import stream_thinking_and_answer, display_panel
from prompts import query_writer_instructions, summarizer_instructions, get_current_date


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

def generate_search_query(research_topic):
    """Generate an effective search query for the research topic."""
    console.print("[bold blue]Generating optimal search query...[/]")

    # Format the prompt
    current_date = get_current_date()

    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=research_topic
    )
    
    messages = [
        SystemMessage(content=formatted_prompt),
        HumanMessage(content=f"Research topic: {research_topic}")
    ]
    
    # Stream the model's thinking process
    console.print("\n[bold]Query Generation Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, query = stream_thinking_and_answer(response_stream, "🔍 Query Generation Thinking")
    
    display_panel(console, f"**Search Query**: {query}", "🔍 Generated Search Query", "green")
    
    return query

def perform_web_search(query):
    """Perform a web search using the Tavily API."""
    console.print("\n[bold blue]Performing web search...[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Searching the web...", total=None)
        search_results = tavily_client.search(query=query, max_results=3)
    
    # Display search result snippets
    console.print("\n[bold]Search Results:[/]")
    for i, result in enumerate(search_results["results"], 1):
        display_panel(
            console,
            f"**Title**: {result['title']}\n\n**Snippet**: {result['content']}\n\n**URL**: {result['url']}",
            f"Result {i}",
            "blue"
        )
    
    return search_results

def summarize_search_results(research_topic, search_results):
    """Summarize the information from search results."""
    console.print("\n[bold blue]Synthesizing information from search results...[/]")
    
    # Format search results for the model
    formatted_results = ""
    for i, result in enumerate(search_results["results"], 1):
        formatted_results += f"Source {i}: {result['title']}\n"
        formatted_results += f"URL: {result['url']}\n"
        formatted_results += f"Content: {result['content']}\n\n"
    
    messages = [
        SystemMessage(content=summarizer_instructions),
        HumanMessage(content=f"Research Topic: {research_topic}\n\nSearch Results:\n{formatted_results}")
    ]
    
    # Stream the model's thinking process for summarization
    console.print("\n[bold]Summarization Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, summary = stream_thinking_and_answer(response_stream, "📝 Summarization Thinking")
    
    display_panel(console, summary, "📝 Research Summary", "green")
    
    return summary

def conduct_research(research_topic):
    """Conduct multi-step research on a topic."""
    console.print(f"[bold]Starting research on: [green]{research_topic}[/green][/]\n")
    
    # Generate search query (use the research topic for first iteration)
    query = generate_search_query(research_topic)
    # Perform web search
    search_results = perform_web_search(query)
    
    # Summarize search results
    summary = summarize_search_results(research_topic, search_results)
    
    return summary

def main():
    """Main function to run the web research demo."""
    console.print("[bold blue]===== Deep Research: Web Research Integration Demo =====\n")
    
    console.print("[yellow]This demo shows how AI models can be enhanced with web search capabilities.")
    console.print("[yellow]You'll see query generation, web search, and synthesis.")
    console.print("[yellow]The AI's thinking will be streamed live in real-time at each stage.\n")
    
    while True:
        research_topic = Prompt.ask("[bold green]Enter a research topic[/] (or 'exit' to quit)")
        
        if research_topic.lower() in ("exit", "quit", "q"):
            console.print("\n[bold blue]Thank you for using the Deep Research web integration demo.[/]")
            break
        
        # Conduct research with two iterations
        conduct_research(research_topic)
        
        console.print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()
