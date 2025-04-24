# Lab 1: Reasoning & Model Thoughts

In this lab, you'll learn about reasoning models and how to separate and visualize the AI's thinking process from its final output. This approach gives you insight into the model's reasoning and helps create more transparent AI systems.

## Understanding AI Reasoning

Modern large language models like DeepSeek-R1 and GPT-4o have powerful reasoning capabilities, but they often hide their step-by-step thinking. By explicitly encouraging and capturing this thinking process, we can:

1. Improve the quality of final outputs
2. Debug reasoning errors
3. Build trust through transparency
4. Create educational tools showing "how" the AI thinks

## Lab Overview

In this lab, you'll:

1. Learn about reasoning techniques in LLMs
2. Create a simple terminal application that shows thinking vs output
3. Use special prompting techniques to encourage step-by-step reasoning
4. Format the thinking and output visually for better user experience
5. **See real-time streaming** of the model's thoughts as they develop

## The Code

The Python application in `lab1_reasoning.py` demonstrates reasoning with visible thoughts:

```python
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

# ... abbreviated for clarity ...
```

The code creates a terminal-based application that:

1. Connects to Azure OpenAI using your credentials
2. Takes research questions as input
3. Uses a special system prompt to encourage the model to "think aloud"
4. **Streams the thinking process in real-time** as the model generates it
5. Formats the final answer as bullet points for clarity
6. Presents the results in styled panels

## Key Components

### System Prompt

The system prompt instructs the model to show its reasoning:

```python
SYSTEM_PROMPT = """You are a research assistant that thinks carefully about questions before answering.

When you receive a research question, first think about the problem step-by-step.
Place all your reasoning and thinking inside <think>...</think> tags.

After thinking, provide your final answer without the thinking tags in bullet points.
Make sure to include all the important details in your answer.
"""
```

This prompt:
- Establishes the model's role as a research assistant
- Provides explicit instructions for structuring output
- Uses XML-like tags (`<think>...</think>`) to demarcate thinking
- Requires bullet points in the final answer for better readability

### Real-Time Streaming

The application streams the model's thinking in real-time using the `stream_thinking_and_answer` function:

```python
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
            # ... process each token as it arrives ...
```

This function:
- Creates a live updating panel using Rich's `Live` context manager 
- Processes each token as it comes from the model
- Distinguishes between thinking sections and the final answer
- Updates the display in real-time with each new token

## Running the Application

To run the application:

1. Ensure you have the required packages installed:

```bash
pip install python-dotenv langchain-azure-ai rich
```

2. Create a `.env` file with your Azure OpenAI credentials:

```
AZURE_AI_ENDPOINT=your_azure_openai_endpoint
AZURE_API_KEY=your_azure_openai_key
```

3. Run the script:

```bash
python lab1_reasoning.py
```

4. Enter research questions at the prompt and observe:
   - The model's thinking process streaming live in real-time
   - The final bullet-point answer displayed separately

## Example Usage

When you run the application, you'll see:
1. A prompt asking for your research question
2. A live cyan panel that updates as the model thinks
3. A green panel with the final bullet-point answer

Try questions like:

- "What are the environmental impacts of electric vehicles?"
- "How does quantum computing differ from classical computing?"
- "What factors contribute to biodiversity loss in rainforests?"

## Benefits

This approach of streaming reasoning as it happens offers several advantages:

1. **Transparency**: Users can see how the model is reasoning step-by-step
2. **Engagement**: The live updating creates a more dynamic user experience
3. **Educational Value**: Observe the reasoning patterns of AI in real time
4. **Debugging**: Identify reasoning flaws as they emerge
5. **Trust**: The decision-making is no longer a black box

## Lab Challenges

Now that you understand the basics, try these challenges:

1. **Modify the System Prompt**: Change the prompt to encourage different types of reasoning
2. **Enhance the Visualization**: Add progress bars or animations to the thinking display
3. **Compare Different Models**: Test how different models approach the same question
4. **Add Error Handling**: Improve how the system handles malformed responses or network issues

## Key Takeaways

From this lab, you should understand:

- How to encourage models to expose their reasoning process
- Techniques for streaming AI thinking in real-time
- The value of separating thinking from final outputs
- How to implement a basic research assistant with visible thinking

## Next Steps

Ready to add web research capabilities to your AI research assistant? Move on to [Lab 2: Web Research Integration](lab-2-web-research.md).