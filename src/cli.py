#!/usr/bin/env python3
"""
Interactive CLI for querying the RAG agent.
Provides a while loop for continuous querying with markdown formatted output.
"""
import typer
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from loguru import logger
from api.agent.graph import run_agent_wrapper

app = typer.Typer()
console = Console()


def display_result(result: dict):
    """Display the result with answer and references."""
    # Display answer as markdown
    console.print("\n[bold cyan]Answer:[/bold cyan]")
    md = Markdown(result.get("answer", "No answer generated"))
    console.print(md)
    
    # Display references if available
    used_context = result.get("used_context", [])
    if used_context:
        console.print("\n[bold cyan]References:[/bold cyan]")
        for i, item in enumerate(used_context, 1):
            console.print(f"\n[yellow]{i}.[/yellow] {item.get('description', 'N/A')}")
            if item.get('price'):
                console.print(f"   [dim]Price: {item.get('price')}[/dim]")
            if item.get('image_url'):
                console.print(f"   [dim]Image: {item.get('image_url')}[/dim]")


def run_query(query: str):
    """Run a single query and return the result."""
    console.print("\n[cyan]Searching...[/cyan]")
    logger.info(f"Query executed: {query}")
    result = run_agent_wrapper(query)
    display_result(result)


def interactive_mode():
    """Run the interactive CLI loop."""
    console.print(
        "[bold cyan]Welcome to the RAG Agent CLI[/bold cyan]\n"
        "[yellow]Type 'exit' or 'quit' to leave[/yellow]\n"
    )
    
    while True:
        try:
            # Get user query
            query = console.input("[bold green]Query:[/bold green] ").strip()
            
            # Check for exit commands
            if query.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            # Skip empty queries
            if not query:
                console.print("[red]Please enter a query[/red]\n")
                continue
            
            # Execute query
            run_query(query)
            console.print()  # Blank line for readability
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]\n")


@app.command()
def main(
    query: Optional[str] = typer.Option(
        None,
        "--query",
        help="Query to execute. If provided, runs once and exits. If not provided, enters interactive mode."
    )
):
    """RAG Agent CLI for querying Amazon products"""
    try:
        if query:
            # Single query mode
            run_query(query)
        else:
            # Interactive mode
            interactive_mode()
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
