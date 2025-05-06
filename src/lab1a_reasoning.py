import os
from dotenv import load_dotenv
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from azure.core.credentials import AzureKeyCredential
from langchain_core.messages import HumanMessage
from rich.prompt import Prompt


# Load environment variables
load_dotenv()

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
        # Create the messages for the AI model
        messages = [
            HumanMessage(content=research_query)
        ]

        response = model.stream(messages)
        
        for chunk in response:
            # Print the chunk of text
            print(chunk.content, end='', flush=True)

if __name__ == "__main__":

    user_input = Prompt.ask("[bold cyan]Enter a research topic[/bold cyan]")
    run_deep_seek(user_input)
