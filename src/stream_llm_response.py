from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live

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

def display_panel(console, content, title, style="green"):
    """Display content in a styled panel."""
    console.print(Panel(
        Markdown(content),
        title=title,
        title_align="left",
        border_style=style,
        padding=(1, 2),
        expand=False
    ))

# Helper function to strip thinking tokens
def strip_thinking_tokens(text: str):
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
