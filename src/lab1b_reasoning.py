import os
from dotenv import load_dotenv
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_core.messages import HumanMessage, SystemMessage
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt

from stream_llm_response import stream_thinking_and_answer

# Load environment variables
load_dotenv()

# Initialize the console for pretty terminal output
console = Console()

endpoint = os.getenv("AZURE_INFERENCE_ENDPOINT")
model_name = os.getenv("AZURE_DEEPSEEK_DEPLOYMENT")
key = os.getenv("AZURE_AI_API_KEY")

# Set up the model
model = AzureAIChatCompletionsModel(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
    model_name=model_name,  
)

def run_deep_seek(research_query):
        
        # The system prompt that instructs the model on how to behave 
        SYSTEM_PROMPT = """You are a research assistant that thinks carefully about questions before answering.

        When you receive a research question, first think about the problem step-by-step.

        After thinking, provide your final answer in bullet points.
        Make sure to include all the important details in your answer.
        """
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
        return answer 


def main():
    """
    Main function to handle the research query and display the AI's thinking and answer.
    """
    console.print("[bold blue]===== Deep Research: AI Thinking & Reasoning Demo =====\n")
    
    console.print("[yellow]This demo shows how Reasoning models can expose their thinking process.")
    console.print("[yellow]You'll see both the model's step-by-step thinking and its final answer.\n")
    
    while True:
        # Get the research query from the user
        research_query = Prompt.ask("[bold green]Enter a research question[/] (or 'exit' to quit)")
        
        if research_query.lower() in ("exit", "quit", "q"):
            console.print("\n[bold blue]Thank you for using the Deep Research reasoning demo.[/]")
            break

        answer = run_deep_seek(research_query)
        
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
