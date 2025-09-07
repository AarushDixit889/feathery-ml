"""
Blueprint: Utils - Banner Generator

This module provides utilities for generating stylized banners and text displays.
"""

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def create_banner(text: str = "FeatheryML", style: str = "slant") -> Panel:
    """
    Create a stylized banner with the given text.
    
    Args:
        text: Text to display in banner
        style: Figlet font style to use
        
    Returns:
        Panel: Rich panel containing the styled banner
    """
    try:
        # Create figlet text
        figlet = pyfiglet.Figlet(font=style)
        ascii_art = figlet.renderText(text)
        
        # Create panel with banner
        return Panel(
            f"[bold cyan]{ascii_art}[/bold cyan]",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        )
        
    except Exception as e:
        console.print(f"[red]Error creating banner: {str(e)}[/red]")
        # Fallback to simple text
        return Panel(
            f"[bold cyan]{text}[/bold cyan]",
            box=box.ROUNDED,
            border_style="blue",
            padding=(1, 2)
        )
