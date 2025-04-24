# Lab 4: Deploying Your Research Assistant

In this lab, you'll transform your terminal-based research assistant into a professional web application using FastAPI and WebSockets. This web interface provides a more user-friendly experience with real-time research updates and a polished UI.

## Understanding Web Application Deployment

Moving from a command-line tool to a web application offers several advantages:

1. **User Accessibility**: Anyone can use the application through a web browser
2. **Real-time Updates**: WebSockets enable live streaming of research progress
3. **Professional Presentation**: A well-designed UI enhances the research experience
4. **Scalability**: The application can be deployed to cloud services for broader access

## Lab Overview

In this lab, you'll:

1. Learn about the FastAPI web framework
2. Set up a WebSocket connection for real-time streaming
3. Create a research workflow using a state graph
4. Deploy a responsive web interface
5. See all previous lab techniques integrated into a production-ready application

## Architecture Overview

The web application uses a modern architecture:

1. **Backend**: FastAPI Python server with WebSocket support
2. **Frontend**: HTML/CSS/JavaScript with Tailwind CSS for styling
3. **State Management**: LangGraph for structured AI workflow orchestration
4. **Data Flow**: Real-time bidirectional communication via WebSockets

![Web App Architecture](media/lab4_architecture.jpg)

## Key Components

### FastAPI Application

The main application in `app/main.py` serves as the backend server:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langgraph.graph import StateGraph, START, END
# ... other imports ...

app = FastAPI(title="Azure Deep Research")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")
```

### Research Graph with LangGraph

The application uses LangGraph to create a structured research workflow:

```python
def setup_graph():
    # Add nodes and edges
    builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput)
    builder.add_node("generate_query", generate_query)
    builder.add_node("web_research", web_research)
    builder.add_node("summarize_sources", summarize_sources)
    builder.add_node("reflect_on_summary", reflect_on_summary)
    builder.add_node("finalize_summary", finalize_summary)
    
    # Add edges
    builder.add_edge(START, "generate_query")
    builder.add_edge("generate_query", "web_research")
    builder.add_edge("web_research", "summarize_sources")
    builder.add_edge("summarize_sources", "reflect_on_summary")
    builder.add_conditional_edges("reflect_on_summary", route_research)
    builder.add_edge("finalize_summary", END)
    
    return builder.compile()
```

This creates a research graph with:
1. Query generation
2. Web research retrieval
3. Information summarization
4. Knowledge gap reflection
5. Multiple research cycles
6. Final report generation

### WebSocket Communication

Real-time updates are provided through WebSockets:

```python
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    manager.connect(websocket, client_id)
    try:
        # Set up the graph
        graph = setup_graph()
        
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            
            if data_json.get("type") == "research":
                # ... start research process ...
                
                async def stream_graph_updates():
                    # ... stream updates to client ...
                    
                # Run graph execution in the background
                asyncio.create_task(stream_graph_updates())
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

### Interactive Web Interface

The web interface in `app/templates/index.html` provides a clean, responsive UI:

- Research topic input
- Real-time progress indicators
- Live streaming of research steps
- Formatted research report display
- "AI Thinking" modal to show reasoning process

## Running the Application

To launch the web application:

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

3. Open your browser and navigate to:

```
http://localhost:8000
```

## Using the Web Interface

The web application features a clean, intuitive interface:

1. **Research Input**: Enter a research topic in the input field and click "Research"
2. **Progress Tracking**: Watch as the system progresses through each research step
3. **Live Updates**: See real-time updates as the research is conducted
4. **Thinking Process**: Click the thought bubble icon to view the AI's reasoning process
5. **Final Report**: View the comprehensive research report with citations

## Behind the Scenes

When a user submits a research topic, the application:

1. Initializes a WebSocket connection for real-time communication
2. Creates a research graph using LangGraph
3. Executes the research workflow in a structured way:
   - Generates an effective search query with visible thinking
   - Performs web searches using the Tavily API
   - Synthesizes information from search results
   - Identifies knowledge gaps and creates follow-up queries
   - Conducts multiple research cycles (up to 3 by default)
   - Compiles a final research report with images and sources
4. Streams progress updates to the client in real-time
5. Displays the final research report with proper formatting

## Deployment Options

After testing locally, you can deploy the application to various platforms:

### Azure App Service

1. Create an Azure App Service with Python support
2. Set up your environment variables in the App Service configuration
3. Deploy your code using Azure DevOps, GitHub Actions, or direct deployment

### Docker Deployment

1. Create a Dockerfile in your project root:

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run the Docker container:

```bash
docker build -t azure-deep-research .
docker run -p 8000:8000 -d azure-deep-research
```

## Enhancing Your Application

Consider these enhancements for your research assistant:

1. **User Authentication**: Add user accounts and save research history
2. **Database Integration**: Store research reports for later reference
3. **Research Export**: Add options to export as PDF or other formats
4. **Custom Research Settings**: Allow users to adjust research depth and sources
5. **Document Upload**: Enable research based on uploaded documents

## Lab Challenges

Try these challenges to extend your learning:

1. **Add Visualization**: Integrate data visualization for numerical research topics
2. **Implement Caching**: Add result caching to improve performance
3. **Multi-Language Support**: Add translation capabilities for multiple languages
4. **Citation Management**: Implement formal academic citation formats
5. **Image Analysis**: Add capabilities to analyze images found during research

## Key Takeaways

From this lab, you should understand:

- How to deploy an AI research assistant as a web application
- Using WebSockets for real-time communication
- Implementing a structured workflow with LangGraph
- Creating an interactive user interface for research
- Integrating all previous lab techniques into a production application

## Congratulations!

You've successfully built and deployed a sophisticated AI research assistant using Azure OpenAI, LangGraph, and FastAPI. This application demonstrates modern AI techniques including:

- Transparent thinking and reasoning
- Web search integration
- Knowledge gap identification
- Iterative research cycles
- Real-time progress streaming

Your application now provides a powerful research tool that can help users explore any topic with the assistance of advanced AI capabilities.