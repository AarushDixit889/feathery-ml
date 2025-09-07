"""
Blueprint: Main CLI Interface

This module serves as the primary entry point for the Feathery ML CLI tool.
It handles project initialization, analysis queries, and project management.

Commands:
1. init: Initialize new statistical analysis project
2. analyze: Run analysis queries
3. commit: Commit changes to git
4. config: Configure project settings
"""

import typer
import inquirer
from typing import Optional, Dict, Any
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import print as rprint
from rich.table import Table
from rich import box

from ..utils.banner import create_banner

from ..project_manager.project_initializer import ProjectInitializer
from ..project_manager.query_manager import QueryManager
from ..git_manager.git_controller import GitController
from ..config_manager.config_handler import ConfigHandler
from ..utils.logger import setup_logger

# Initialize logger and console
logger = setup_logger(__name__)
console = Console()

# Display banner on startup
console.print(create_banner())

# Create Typer app instance with rich formatting
app = typer.Typer(
    help="[bold green]🪽 Feathery ML:[/bold green] AI-powered statistical analysis tool",
    no_args_is_help=True
)

@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the statistical analysis project"),
    path: str = typer.Option(".", help="Path where project should be created"),
    use_git: bool = typer.Option(True, help="Initialize git repository")
):
    """
    Initialize a new statistical analysis project with the standard structure.
    
    Creates:
    1. Project directory structure
    2. Git repository (optional)
    3. Configuration file
    4. QnA history file
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Initialize project
            task_init = progress.add_task(
                "[bold blue]Initializing project...", total=None
            )
            initializer = ProjectInitializer(project_name, Path(path))
            project_path = initializer.create_project()
            progress.update(task_init, completed=True)
            
            # Initialize git if requested
            if use_git:
                task_git = progress.add_task(
                    "[bold yellow]Setting up git repository...", total=None
                )
                git_controller = GitController(project_path)
                git_controller.init_repository()
                progress.update(task_git, completed=True)
        
        # Show success message
        success_panel = Panel(
            f"[green]Project initialized successfully at:[/green]\n{project_path}",
            title="✨ Project Created",
            border_style="green"
        )
        console.print(success_panel)
        
        # Show project structure
        structure_table = Table(
            title="Project Structure",
            box=box.ROUNDED,
            show_header=False,
            title_style="bold blue"
        )
        structure_table.add_column("Path", style="dim")
        
        structure = [
            "📁 data/",
            "  └─📁 raw/",
            "  └─📁 processed/",
            "📁 src/",
            "📄 qna.json",
            "📄 .feathers"
        ]
        
        for item in structure:
            structure_table.add_row(item)
        
        console.print(structure_table)
        
    except Exception as e:
        logger.error(f"Project initialization failed: {str(e)}")
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def analyze(
    query: str = typer.Argument(None, help="Natural language query for analysis"),
    save: bool = typer.Option(True, help="Save changes to git after analysis"),
    chat: bool = typer.Option(False, "--chat", "-c", help="Start interactive chat session")
):
    """
    Run statistical analysis based on natural language query.
    
    Modes:
    1. Single query mode: Provide query as argument
    2. Chat mode: Interactive session with --chat flag
    
    Steps:
    1. Process query/start chat session
    2. Generate and execute analysis code
    3. Save results
    4. Update QnA history
    5. Optionally commit changes
    """
    try:
        if chat:
            # Start interactive chat session
            from ..chat_manager.chat_session import ChatSession
            session = ChatSession(auto_commit=save)
            session.start_session()
        else:
            # Single query mode
            if not query:
                raise typer.BadParameter("Query is required in non-chat mode")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                # Process query
                task = progress.add_task("[bold blue]Processing analysis...", total=None)
                query_manager = QueryManager()
                result = query_manager.process_query(query)
                progress.update(task, completed=True)
            
            # Display code with syntax highlighting
            console.print("\n[bold green]Generated Code:[/bold green]")
            code_panel = Panel(
                Syntax(result.code, "python", theme="monokai", line_numbers=True),
                border_style="green"
            )
            console.print(code_panel)
            
            # Display results
            console.print("\n[bold blue]Results:[/bold blue]")
            result_panel = Panel(
                str(result.result),
                border_style="blue"
            )
            console.print(result_panel)
            
            if save:
                with console.status("[bold yellow]Committing changes..."):
                    git_controller = GitController()
                    git_controller.commit_changes(f"Analysis: {query}")
                console.print("[green]Changes committed successfully![/green]")
            
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

@app.command()
def commit(
    message: str = typer.Option(None, help="Commit message"),
    push: bool = typer.Option(False, help="Push changes after commit")
):
    """
    Commit changes to git repository.
    
    Options:
    1. Custom commit message
    2. Auto-push to remote
    """
    try:
        git_controller = GitController()
        git_controller.commit_changes(message)
        
        if push:
            git_controller.push_changes()
            
    except Exception as e:
        logger.error(f"Git operation failed: {str(e)}")
        raise typer.Exit(1)

@app.command()
def config(
    set_key: str = typer.Option(None, help="Set configuration key"),
    set_value: str = typer.Option(None, help="Set configuration value")
):
    """
    Configure project settings.
    
    Operations:
    1. View current configuration
    2. Set configuration values
    3. Reset configuration
    """
    try:
        config_handler = ConfigHandler()
        
        if set_key and set_value:
            with console.status("[bold blue]Updating configuration..."):
                config_handler.set_config(set_key, set_value)
            console.print(f"[green]Configuration updated:[/green] {set_key} = {set_value}")
        else:
            config = config_handler.get_config()
            
            # Display configuration in a table
            table = Table(
                title="Current Configuration",
                box=box.ROUNDED,
                header_style="bold magenta"
            )
            table.add_column("Key", style="bold blue")
            table.add_column("Value", style="green")
            
            for key, value in config.items():
                table.add_row(str(key), str(value))
            
            console.print(table)
            
    except Exception as e:
        logger.error(f"Configuration failed: {str(e)}")
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1)

def main():
    """Entry point for the CLI application"""
    app()
