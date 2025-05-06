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
from prompts import query_writer_instructions, get_current_date


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

        # Perform the search
        search_results = tavily_client.search(query=query, max_results=1, search_depth='basic')
    
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

def main():
    """Main function to run the web research demo."""
    console.print("[bold blue]===== Deep Research: Query Generation and Web Research =====\n")
    
    while True:
        research_topic = Prompt.ask("[bold green]Enter a research topic[/] (or 'exit' to quit)")
        
        if research_topic.lower() in ("exit", "quit", "q"):
            console.print("\n[bold blue]Thank you for using the Deep Research web integration demo.[/]")
            break
        
        # Generate search query (use the research topic for first iteration)
        query = generate_search_query(research_topic)
        # Perform web search
        search_results = perform_web_search(query)
        
        console.print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()