import os
import time
from dotenv import load_dotenv
from typing import Tuple
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live

# Load environment variables
load_dotenv()

# Initialize the console for pretty terminal output
console = Console()

# Set up the AI model
model = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_AI_ENDPOINT"),
    credential=os.getenv("AZURE_API_KEY"),
    model_name="DeepSeek-R1",  
)

# The system prompt that instructs the model to show its thinking process
SYSTEM_PROMPT = """You are a research assistant that thinks carefully about questions before answering.

When you receive a research question, first think about the problem step-by-step.
Place all your reasoning and thinking inside <think>...</think> tags.

After thinking, provide your final answer without the thinking tags in bullet points.
Make sure to include all the important details in your answer.


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

def main():
    """
    Main function to handle the research query and display the AI's thinking and answer.
    """
    console.print("[bold blue]===== Deep Research: AI Thinking & Reasoning Demo =====\n")
    
    console.print("[yellow]This demo shows how AI models can expose their reasoning process.")
    console.print("[yellow]You'll see both the model's step-by-step thinking and its final answer.\n")
    
    while True:
        # Get the research query from the user
        research_query = Prompt.ask("[bold green]Enter a research question[/] (or 'exit' to quit)")
        
        if research_query.lower() in ("exit", "quit", "q"):
            console.print("\n[bold blue]Thank you for using the Deep Research reasoning demo.[/]")
            break
        
        # Create the messages for the AI model
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=research_query)
        ]
        
        # Show a spinner while waiting for the AI response
        with console.status("[bold blue]AI is thinking...", spinner="dots"):
            response = model.stream(messages)
        
        # Extract the thinking process and the final answer
        thoughts, answer = stream_thinking_and_answer(response)
        
        # Display  answer in styled panels
        console.print("\n[bold]Results:[/]\n")
        console.print(Panel(
        Markdown(answer),
        title="📝 Research Answer",
        title_align="left",
        border_style="green",
        padding=(1, 2),
        expand=False
        ))
        console.print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()