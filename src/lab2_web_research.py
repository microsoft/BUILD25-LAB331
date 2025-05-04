import os
import json
import time
import dotenv
from typing import Dict, List, Any, Tuple
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

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

# System prompts for different stages of research
QUERY_GENERATION_PROMPT = """You are an expert at generating effective search queries.

When given a research topic, generate the optimal search query that will find the most relevant and useful information. The query should be specific enough to find relevant information but not so narrow that it misses important context.

Place your thinking process inside <think>...</think> tags, and then provide just the search query as your final answer.

For example:
User: Research the impact of climate change on marine ecosystems

You: <think>
For this research topic on climate change's impact on marine ecosystems, I need to craft a query that will bring up recent and relevant scientific information. I should include:
- The main topic "climate change" and "marine ecosystems"
- Some specific effects that would be relevant like "ocean acidification", "coral bleaching", "sea level rise"
- Terms that would find scientific or research-based sources
- I should avoid terms that are too general or would bring up basic information
</think>

climate change impacts marine ecosystems ocean acidification coral bleaching scientific research recent findings
"""

SUMMARIZATION_PROMPT = """You are a research assistant that creates comprehensive summaries from web search results.

Given the search results provided, create a detailed and informative summary that:
1. Synthesizes the key information from all sources
2. Organizes information logically
3. Highlights important facts, statistics, and findings
4. Maintains accuracy and avoids adding unfounded information
5. Cites sources appropriately

Place your thinking process inside <think>...</think> tags, and then provide your final summary.
"""

def stream_thinking_and_answer(stream_generator, title="🧠 AI Thinking Process (Live)"):
    """
    Stream the AI's thinking and answer in real-time, separating them visually.
    """
    # Containers for accumulating thoughts and answer
    accumulated_thoughts = ""
    accumulated_answer = ""
    in_thinking_section = False
    
    thinking_panel = Panel(
        Markdown(""),
        title=title,
        title_align="left",
        border_style="cyan",
        padding=(1, 2),
        expand=False
    )
    
    with Live(thinking_panel, refresh_per_second=4) as live:
        for chunk in stream_generator:
            content = chunk.content if hasattr(chunk, 'content') else chunk
            if not content:
                continue
            
            # Check for thinking tags
            if "<think>" in content:
                in_thinking_section = True
                content = content.replace("<think>", "")
            if "</think>" in content:
                in_thinking_section = False
                content = content.replace("</think>", "")
                accumulated_thoughts += content
                
                # Update the live display with the latest thoughts
                thinking_panel.renderable = Markdown(accumulated_thoughts)
                live.update(thinking_panel)
                continue
            
            # Add content to the appropriate section
            if in_thinking_section:
                accumulated_thoughts += content
                
                # Update the live display with the latest thoughts
                thinking_panel.renderable = Markdown(accumulated_thoughts)
                live.update(thinking_panel)
            else:
                accumulated_answer += content
    
    return accumulated_thoughts, accumulated_answer

def display_panel(content, title, style="green"):
    """Display content in a styled panel."""
    console.print(Panel(
        Markdown(content),
        title=title,
        title_align="left",
        border_style=style,
        padding=(1, 2),
        expand=False
    ))

def generate_search_query(research_topic):
    """Generate an effective search query for the research topic."""
    console.print("[bold blue]Generating optimal search query...[/]")
    
    messages = [
        SystemMessage(content=QUERY_GENERATION_PROMPT),
        HumanMessage(content=f"Research topic: {research_topic}")
    ]
    
    # Stream the model's thinking process
    console.print("\n[bold]Query Generation Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, query = stream_thinking_and_answer(response_stream, "🔍 Query Generation Thinking")
    
    display_panel(f"**Search Query**: {query}", "🔍 Generated Search Query", "green")
    
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
        search_results = tavily_client.search(query=query, search_depth="advanced", max_results=5)
    
    # Display search result snippets
    console.print("\n[bold]Search Results:[/]")
    for i, result in enumerate(search_results["results"], 1):
        display_panel(
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
        SystemMessage(content=SUMMARIZATION_PROMPT),
        HumanMessage(content=f"Research Topic: {research_topic}\n\nSearch Results:\n{formatted_results}")
    ]
    
    # Stream the model's thinking process for summarization
    console.print("\n[bold]Summarization Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, summary = stream_thinking_and_answer(response_stream, "📝 Summarization Thinking")
    
    display_panel(summary, "📝 Research Summary", "green")
    
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
    
    # # Compile final research report from all summaries
    # console.print("\n[bold]===== Final Research Report =====[/]\n")
    
    # final_report = f"# Research Report: {research_topic}\n\n"
    # for i, summary in enumerate(all_summaries, 1):
    #     final_report += f"## Research Cycle {i}\n\n{summary}\n\n"
    
    # display_panel(final_report, "📊 Complete Research Report", "purple")
    
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
