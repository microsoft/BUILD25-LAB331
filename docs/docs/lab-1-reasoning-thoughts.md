# Lab 1: Reasoning & Model Thoughts

In this lab, you'll learn about reasoning models and how to separate the LLM's thinking process from its final output. 

## What is a Reasoning Model? 

Reasoning models, like DeepSeek-R1, are LLMs trained with reinforcement learning to perform reasoning. Reasoning models think before they answer, producing a long internal chain of thought before responding to the user [[source](https://platform.openai.com/docs/guides/reasoning?utm_source=chatgpt.com&api-mode=responses)]. They often outperform vanilla chat models on tasks like multi‑step math, code debugging, planning, tool use, and long‑context question‑answering. 

When combined with a tool to access the web, Reasoning models are particularly good at research. Their chain‑of‑thought training and reward signals make them better at spotting gaps, cross‑checking sources, and iterating on hypotheses. Some popular reasoing models are DeepSeek R1, OpenAI's o3 and o1, and Microsoft's Ph-4-reasoning.

## Lab Overview

In this lab, you'll:

1. Learn how to use a reasoning model by looking at the raw output.
2. Learn how to seperate the models thinking vs final output. 
3. Update the models system prompt to get formatted output.

## Getting started with DeepSeek R1

To access DeepSeek R1 we will be using [langchain-azure-ai](https://pypi.org/project/langchain-azure-ai/), the official Python package that contains most Langchains Azure integrations. This package leverages [Azure AI's Inference SDK](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-inference-readme?view=azure-python-preview) to give us access to all the models available in [Azure AI Foundry](https://ai.azure.com/) using Langchain. 

To get started in the VS Code terminal and run the following command and enter a research topic, for example 'What's the best coffee in Seattle?':

```powershell
python lab1a_reasoning.py
```

Look at the output in the terminal. What do you notice about the answer this model returns vs what a chat model would typically output? 
Open the file [lab1a_reasoning.py](../../src/lab1a_reasoning.py) and examine the code. Note that we do not pass a system prompt and the instructions for the model to think are built in. 

Type in 'exit' to leave the program and continue with the next step. 

## Seperating Thinking from the Final Answer

The output from the model in the previous step contains the models thinking. This output might be helpful for developers and the curious but might not always be helpful when building an application where users only expect the final output. 

Many reasoning models like DeepSeek R1 put the models thought process in thinking tags that look like this `<think> </think>`. In order to seperate the models thinking from it's final answer we can create helper function in Python to seperate the thinking from the final output. This is what the code to this would look like:

```python
def seperate_thinking_from_final_output(text: str):
    """
    Extract the content between <think> and </think> tags and remove them from the text.
    """
    thoughts = ""
    while "<think>" in text and "</think>" in text:
        start = text.find("<think>")
        end = text.find("</think>")
        # Extract the content between tags (excluding the tags themselves)
        thoughts += text[start + len("<think>"):end].strip() + "\n\n"
        # Remove the tags and their content from the original text
        text = text[:start] + text[end + len("</think>"):]
    return thoughts.strip(), text.strip()
```

Look at the code in the [stream_llm_response.py](../../src/stream_llm_response.py) file. It contains a slightly updated version of this helper function in the `stream_thinking_and_answer` function. This helper function will be imported in all our python files going forward. It also contains some code that uses the Python package [rich](https://pypi.org/project/rich/) for prettier display in the terminal. 

To test this code out run the following command in the terminal. 

```powershell
python lab1b_reasoning.py
```

!!! note
    The final output is returned as bullet points. This format can be specified in the models system prompt. Try updating the system prompt in [lab1b_reasoning.py](../../src/lab1b_reasoning.py) to test out a different format like in a table format, for example:


    ```python
    SYSTEM_PROMPT = """You are a research assistant that thinks carefully about questions before answering.

    When you receive a research question, first think about the problem step-by-step.

    After thinking, provide your final answer in a helpful table format.
    Make sure to include all the important details in your answer.
    """
    ```

## Next Steps

Congratulations, you should now feel comfortable using reasoning models! 
You are now ready to move on to [Lab 2: Web Research Integration](lab-2-web-research.md).