# Lab 3: Research Reflection

## Understanding Research Reflection

Even with web search capabilities, a single research cycle often leaves important questions unanswered. Real research is iterative - findings from initial searches reveal what else we need to know.

Research reflection involves:

1. **Knowledge Gap Identification**: Analyzing current information to find what's missing
2. **Follow-up Query Generation**: Creating targeted follow-up questions to fill these gaps
3. **Multiple Research Cycles**: Conducting iterative research to build comprehensive knowledge
4. **Progressive Synthesis**: Combining findings from all iterations into a coherent whole

## When To Use An AI Framework

This process will give us the high quality results but veers away from the linear flow of the scripts we saw in the previous labs. As AI workflows become more complex, developers need to write code that takes into account things like states, conditional branching, tool use and more. To simplify this process it is often useful to use an AI framework. [LangGraph](https://www.langchain.com/langgraph) is a Python framework that lets you build stateful, multi-step reasoning workflows using large language models by representing them as graphs. It’s built on top of LangChain and designed for more complex use cases.

## Using LangGraph For The Iterative Research Process

![Iterative Research Process](media/deep_research_outline_image.png)

The complete iterative **'Deep Research'** process includes:

1. Initial query generation and web search 
2. Summarization of web search results into a report
4. Knowledge gap identification after initial research
5. Follow-up search cycles based on identified gaps
4. Synthesis of all findings into a comprehensive report





🧠 Key Concepts:
Graph Nodes = individual steps (e.g. call an LLM, retrieve docs, update memory)

Edges = the transitions between those steps, which can depend on model outputs

State = shared memory or variables passed between steps

Loops & Branching = supports revisiting steps or changing paths based on conditions

✅ Why use LangGraph?
Lets you orchestrate reasoning over multiple steps

You can build agents that loop, retry, reflect, or use tools based on context

Better suited than standard LangChain chains for dynamic, evolving conversations

It handles state management, asynchronous execution, and tool usage elegantly






## The Code

The Python application in `lab3_reflection.py` extends our Lab 2 implementation with knowledge gap identification and iterative research:

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

### Knowledge Gap Identification

After the initial research cycle, the system analyzes what information is missing:

```python
def identify_knowledge_gaps(research_topic, current_summary):
    """Identify knowledge gaps and generate a follow-up query."""
    console.print("\n[bold blue]Identifying knowledge gaps...[/]")
    
    messages = [
        SystemMessage(content=REFLECTION_PROMPT),
        HumanMessage(content=f"Research Topic: {research_topic}\n\nCurrent Summary:\n{current_summary}")
    ]
    
    # Stream the model's thinking process for knowledge gap identification
    console.print("\n[bold]Knowledge Gap Analysis Process:[/]\n")
    response_stream = model.stream(messages)
    thoughts, json_str = stream_thinking_and_answer(response_stream, "🔍 Reflection Thinking")
    
    # Try to parse the JSON response
    try:
        reflection = json.loads(json_str)
        knowledge_gap = reflection.get("knowledge_gap", "No specific knowledge gap identified.")
        follow_up_query = reflection.get("follow_up_query", f"More information about {research_topic}")
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        knowledge_gap = "Unable to parse the identified knowledge gap."
        follow_up_query = f"More information about {research_topic}"
    
    display_panel(
        f"**Knowledge Gap**: {knowledge_gap}\n\n**Follow-up Query**: {follow_up_query}",
        "🔍 Knowledge Gap Analysis",
        "yellow"
    )
    
    return knowledge_gap, follow_up_query
```

This function:
- Analyzes the current research summary to identify knowledge gaps
- Generates a specific follow-up query to address the most important gap
- Returns both the knowledge gap description and the follow-up query
- Streams the model's thinking process in real-time

### Multi-Iteration Research

The `conduct_research` function now performs multiple research iterations:

```python
def conduct_research(research_topic, max_iterations=2):
    """Conduct multi-step research on a topic."""
    console.print(f"[bold]Starting research on: [green]{research_topic}[/green][/]\n")
    
    all_summaries = []
    
    for iteration in range(1, max_iterations + 1):
        console.print(f"\n[bold]===== Research Iteration {iteration} =====[/]\n")
        
        # Generate search query (use the research topic for first iteration)
        if iteration == 1:
            query = generate_search_query(research_topic)
        else:
            # For subsequent iterations, use the follow-up query from reflection
            _, query = identify_knowledge_gaps(research_topic, all_summaries[-1])
        
        # Perform web search
        search_results = perform_web_search(query)
        
        # Summarize search results
        summary = summarize_search_results(research_topic, search_results)
        all_summaries.append(summary)
    
    # Compile final research report from all summaries
    console.print("\n[bold]===== Final Research Report =====[/]\n")
    
    final_report = f"# Research Report: {research_topic}\n\n"
    for i, summary in enumerate(all_summaries, 1):
        final_report += f"## Research Cycle {i}\n\n{summary}\n\n"
    
    display_panel(final_report, "📊 Complete Research Report", "purple")
    
    return final_report
```

This function:
- Performs multiple research iterations (default is 2)
- Uses the initial topic for the first search
- Uses knowledge gap analysis to guide subsequent searches
- Compiles all findings into a comprehensive final report

### Research Report Compilation

The final report combines findings from all research iterations:

```python
# Compile final research report from all summaries
console.print("\n[bold]===== Final Research Report =====[/]\n")

final_report = f"# Research Report: {research_topic}\n\n"
for i, summary in enumerate(all_summaries, 1):
    final_report += f"## Research Cycle {i}\n\n{summary}\n\n"

display_panel(final_report, "📊 Complete Research Report", "purple")
```

This creates a well-structured report with sections for each research cycle.

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
python lab3_reflection.py
```

4. Enter a research topic and observe the multi-cycle research process.

## Example Usage

When you run the application and enter a research topic like "quantum computing applications in medicine", you'll see:

1. **First Research Cycle**:
   - Generation of an initial search query
   - Web search results
   - Summary of initial findings

2. **Knowledge Gap Analysis**:
   - Identification of missing information
   - Generation of a follow-up query

3. **Second Research Cycle**:
   - Web search using the follow-up query
   - Summary of additional findings

4. **Final Research Report**:
   - Comprehensive report combining all research cycles

## Benefits of Iterative Research

This approach offers several advantages:

1. **Thoroughness**: Multiple research cycles produce more comprehensive results
2. **Targeted Follow-up**: Each cycle focuses on what's still unknown
3. **Progressive Refinement**: Later cycles build on knowledge from earlier ones
4. **Better Coverage**: Different search queries capture different aspects of the topic
5. **Self-Awareness**: The system acknowledges what it doesn't know

## Lab Challenges

Try these challenges to extend your learning:

1. **Increase Iterations**: Modify the code to perform 3 or more research cycles
2. **Topic Segmentation**: Modify the system to explore different subtopics in parallel
3. **User Guidance**: Add user input between iterations to guide the research direction
4. **Sentiment Analysis**: Add analysis of different perspectives on controversial topics
5. **Citation Improvement**: Create a more formal citation system for sources

## Key Takeaways

From this lab, you should understand:

- How to implement knowledge gap identification
- Techniques for creating targeted follow-up queries
- Methods for conducting multi-cycle research
- The value of iterative approaches in comprehensive research

## Next Steps

Ready to incorporate this research system into a full production application? Move on to [Lab 4: Launching Your Researcher](lab-4-launch-researcher.md).