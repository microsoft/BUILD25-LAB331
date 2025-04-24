# Getting Started

This section will help you set up your environment for the Azure Deep Research Workshop.

## Environment Setup

### 1. Clone the Repository

Start by cloning the workshop repository:

```bash
git clone https://github.com/yourusername/deep-research.git
cd deep-research
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment:

=== "Windows"
    ```powershell
    python -m venv deep_research
    .\deep_research\Scripts\activate
    ```

=== "macOS/Linux"
    ```bash
    python -m venv deep_research
    source deep_research/bin/activate
    ```

### 3. Install Required Packages

Install the necessary Python packages:

```bash
pip install -r requirements.txt
```

The key packages include:
- `langchain-azure-ai` for Azure OpenAI integration
- `tavily-python` for web search capabilities
- `rich` for terminal formatting and UI
- `fastapi` and `uvicorn` for the web application
- `langgraph` for structuring the research workflow

### 4. Set Up Azure OpenAI

To use Azure OpenAI in this workshop, you'll need:

1. An Azure account with access to Azure OpenAI Service
2. A deployment of the following models:
   - DeepSeek-R1 (used for reasoning and research)
   - GPT-4o (optional, used in the web application)

If you don't have access yet, request it through the [Azure OpenAI Service request form](https://aka.ms/oaiapply).

### 5. Set Up Tavily API

Register for a [Tavily API key](https://tavily.com/) to enable web search capabilities. This API is essential for the web research integration in Labs 2 and 3.

### 6. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```
AZURE_AI_ENDPOINT=your_azure_openai_endpoint
AZURE_API_KEY=your_azure_openai_key
TAVILY_API_KEY=your_tavily_api_key
```

These environment variables will be loaded in each lab using the `python-dotenv` package.

## Workshop Materials

This workshop is designed as a progressive series of labs, each building on the previous one:

1. **Lab 1 (Reasoning & Model Thoughts)**: Learn how to stream the AI's thinking process in real-time and format final answers as bullet points.

2. **Lab 2 (Web Research Integration)**: Build a basic research system that generates queries, searches the web, and synthesizes the results.

3. **Lab 3 (Research Reflection)**: Extend the research capabilities with knowledge gap identification and iterative research cycles.

4. **Lab 4 (Launching Your Researcher)**: Deploy the research assistant as a web application with FastAPI and WebSockets for real-time updates.

Each lab includes code samples, explanations, and challenges to extend your learning.

## Navigation

Use the navigation menu on the left to move between labs. Each lab includes:

- An overview of what you'll learn
- Prerequisites specific to that lab
- Detailed instructions with code samples
- Explanations of key components
- Challenges to extend your learning
- Next steps to progress through the workshop

## Next Steps

Once your environment is set up, proceed to [Lab 1: Reasoning & Model Thoughts](lab-1-reasoning-thoughts.md) to begin building your research assistant.