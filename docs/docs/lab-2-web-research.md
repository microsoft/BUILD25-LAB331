# Lab 2: Web Research Integration

In this lab, you'll learn how to enhance your AI research assistant by integrating web search capabilities. This allows the model to access up-to-date information beyond its training data and provide more accurate and comprehensive research results.

## Understanding Web-Connected AI

While large language models have extensive knowledge, they have two major limitations:

1. **Training Data Cutoff**: Models only have knowledge up to their training cutoff date
2. **Knowledge Limitations**: No model knows everything, especially about niche or emerging topics

By connecting your AI to web search capabilities, you can:
- Obtain current information not available during model training
- Get authoritative information from reliable sources
- Research specialized topics where the model's knowledge may be limited
- Find specific data points, statistics, and references

## Lab Overview

In this lab, you'll:

1. Set up the Tavily API for web search
2. Create a focused research process with web search integration
3. Structure and analyze search results
4. Build a script that performs research with an AI-guided search strategy
5. See real-time streaming of the AI's thinking at each stage of the process

## The Web Research Process

The web research integration involves three key components:

1. **Query Generation**: Creating effective search queries based on the research topic
2. **Web Search**: Retrieving relevant information from external sources
3. **Information Synthesis**: Integrating the retrieved information into a cohesive summary

![Web Research Process](media/lab2_research_process.jpg)

## Setting Up Tavily API

In this lab, we'll use the Tavily Search API, which provides AI-optimized web search capabilities. 

1. Sign up for a [Tavily API key](https://tavily.com/)
2. Add your Tavily API key to your `.env` file:

```
TAVILY_API_KEY=your_tavily_api_key
```

## The Code

The Python application in `lab2_web_research.py` builds on our reasoning model from Lab 1 and adds web search capabilities:

```python
import os
import json
import time
import dotenv
from typing import Dict, List, Any, Tuple
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live

# ... abbreviated for clarity ...
```

## Key Components

### Query Generation

The system first generates an optimal search query based on the research topic:

```python
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
```

This function uses a specialized prompt to help the model craft an effective search query, streaming its thinking process in real-time.

### Web Search

The generated query is used to perform a web search using the Tavily API:

```python
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
```

This retrieves information from the web about the topic and displays snippets of the results.

### Information Synthesis

The search results are then summarized into a coherent research overview:

```python
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
```

This synthesizes the search results into a comprehensive summary, again streaming the AI's thinking process.

### Research Orchestration

The `conduct_research` function ties everything together:

```python
def conduct_research(research_topic):
    """Conduct multi-step research on a topic."""
    console.print(f"[bold]Starting research on: [green]{research_topic}[/green][/]\n")
    
    # Generate search query
    query = generate_search_query(research_topic)
    
    # Perform web search
    search_results = perform_web_search(query)
    
    # Summarize search results
    summary = summarize_search_results(research_topic, search_results)
    
    return summary
```

This function orchestrates the complete research process, from query generation to final summary.

## Running the Application

To run the application:

1. Ensure you have the required packages installed:

```bash
pip install python-dotenv langchain-azure-ai tavily-python rich
```

2. Make sure your `.env` file includes both Azure OpenAI and Tavily API keys:

```
AZURE_AI_ENDPOINT=your_azure_openai_endpoint
AZURE_API_KEY=your_azure_openai_key
TAVILY_API_KEY=your_tavily_api_key
```

3. Run the script:

```bash
python lab2_web_research.py
```

4. Enter a research topic and observe the complete research process.

## Example Usage

When you run the application and enter a research topic like "latest advancements in fusion energy", you'll see:

1. The model generating an effective search query with visible thinking
2. Results from the web search with titles and snippets
3. The model synthesizing a summary with visible thinking
4. A final comprehensive research summary

## Lab Challenges

Now that you understand web research integration, try these challenges:

1. **Modify the Search Depth**: Change the Tavily search parameters to get different results
2. **Customize the Prompts**: Adjust the prompts to generate different types of summaries
3. **Add Image Support**: Extend the script to collect and display relevant images from the web
4. **Source Citation**: Enhance the summary to include proper citations for each piece of information

## Key Takeaways

From this lab, you should understand:

- How to connect AI models to external knowledge sources
- Techniques for generating effective search queries
- Methods for synthesizing information from multiple sources
- The power of real-time thinking visualization during each stage

## Next Steps

Ready to extend your research assistant with knowledge gap identification and iterative research? Move on to [Lab 3: Research Reflection](lab-3-reflection.md).