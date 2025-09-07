"""
Blueprint: Chat Manager - Interactive Session

This module provides an interactive chat interface for continuous statistical analysis.
It manages the chat session, history, and query processing flow.

Components:
1. Chat Session Management
2. Interactive Interface
3. History Tracking
4. Context Management
"""

from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.markdown import Markdown
from rich.layout import Layout
from rich import box

from ..utils.banner import create_banner

from ..project_manager.query_manager import QueryManager
from ..git_manager.git_controller import GitController
from ..utils.logger import setup_logger

logger = setup_logger(__name__)
console = Console()

class ChatSession:
    """Manages an interactive chat session for analysis"""
    
    def __init__(self, auto_commit: bool = True):
        """Initialize chat session with components"""
        self.query_manager = QueryManager()
        self.git_controller = GitController() if auto_commit else None
        self.history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.layout = self._setup_layout()
        
    def start_session(self):
        """Start an interactive chat session"""
        self._display_welcome()
        
        while True:
            try:
                # Get query from user
                query = self._get_user_input()
                
                if query.lower() == 'exit':
                    self._end_session()
                    break
                elif query.lower() == 'help':
                    self._show_help()
                    continue
                elif query.lower() == 'history':
                    self._show_history()
                    continue
                
                # Process query and show results
                with console.status("[bold green]Processing analysis..."):
                    result = self.query_manager.process_query(query)
                    self._handle_result(result)
                
                # Auto-commit if enabled
                if self.git_controller:
                    with console.status("[bold yellow]Committing changes..."):
                        self.git_controller.commit_changes(f"Analysis: {query}")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Ending session...[/yellow]")
                break
            except Exception as e:
                logger.error(f"Error in chat session: {str(e)}")
                console.print(f"\n[red]Error:[/red] {str(e)}")
    
    def _setup_layout(self) -> Layout:
        """Setup rich layout for UI"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="input", size=3)
        )
        return layout
    
    def _display_welcome(self):
        """Display welcome message"""
        # Display banner
        console.print(create_banner())
        
        # Display welcome message
        welcome_panel = Panel(
            "[bold green]Welcome to Feathery ML Chat Interface![/bold green]\n"
            "Type [bold]'exit'[/bold] to end session, [bold]'help'[/bold] for commands",
            title="🪽 Interactive Analysis",
            border_style="blue"
        )
        console.print(welcome_panel)
    
    def _get_user_input(self) -> str:
        """Get query from user with enhanced prompt"""
        return Prompt.ask("\n[bold blue]Analysis Query[/bold blue]")
    
    def _handle_result(self, result: Any):
        """Process and display analysis results with syntax highlighting"""
        # Add to history
        self.history.append({
            'query': result.query,
            'timestamp': datetime.now().isoformat(),
            'code': result.code
        })
        
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
    
    def _show_help(self):
        """Display available commands with rich formatting"""
        help_md = """
        # Available Commands
        
        - `exit`: End chat session
        - `help`: Show this help message
        - `history`: Show query history
        
        # Tips
        
        - Be specific in your queries
        - Reference previous results using 'previous analysis'
        - Use natural language for your statistical questions
        
        # Examples
        
        - "Calculate mean and standard deviation of column A"
        - "Plot histogram of age distribution"
        - "Run linear regression of price on square footage"
        """
        console.print(Markdown(help_md))
    
    def _show_history(self):
        """Display session history in a rich table"""
        if not self.history:
            console.print("\n[yellow]No queries in history[/yellow]")
            return
        
        table = Table(
            title="Query History",
            box=box.ROUNDED,
            header_style="bold magenta"
        )
        table.add_column("#", style="dim")
        table.add_column("Query", style="bold")
        table.add_column("Timestamp", style="dim")
        
        for i, entry in enumerate(self.history, 1):
            table.add_row(
                str(i),
                entry['query'],
                entry['timestamp'].split('T')[1][:8]  # Show only time
            )
        
        console.print(table)
    
    def _end_session(self):
        """Clean up and end chat session"""
        # Save final history
        with console.status("[bold green]Saving session history..."):
            self._save_history()
        
        farewell_panel = Panel(
            "[green]Chat session ended. All analyses have been saved.[/green]",
            title="👋 Goodbye!",
            border_style="green"
        )
        console.print(farewell_panel)
    
    def _save_history(self):
        """Save chat history to QnA file"""
        try:
            qna_file = Path.cwd() / "qna.json"
            self.query_manager.bulk_update_history(self.history)
            logger.info("Chat history saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save chat history: {str(e)}")
            raise
