"""
Test suite for core functionality of Feathery ML.
"""

import pytest
from pathlib import Path
import shutil
import json

from src.project_manager.project_initializer import ProjectInitializer
from src.project_manager.query_manager import QueryManager
from src.git_manager.git_controller import GitController
from src.config_manager.config_handler import ConfigHandler
from src.chat_manager.chat_session import ChatSession
from src.utils.banner import create_banner
from rich.panel import Panel

@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project for testing"""
    project_name = "test_project"
    project_path = tmp_path / project_name
    initializer = ProjectInitializer(project_name, tmp_path)
    project_path = initializer.create_project()
    return project_path

def test_project_initialization(tmp_path):
    """Test project structure creation"""
    # Initialize project
    project_name = "test_project"
    initializer = ProjectInitializer(project_name, tmp_path)
    project_path = initializer.create_project()
    
    # Check directory structure
    assert project_path.exists()
    assert (project_path / "data").exists()
    assert (project_path / "data" / "raw").exists()
    assert (project_path / "data" / "processed").exists()
    assert (project_path / "src").exists()
    assert (project_path / "qna.json").exists()
    assert (project_path / ".feathers").exists()

def test_git_initialization(temp_project):
    """Test git repository initialization"""
    git_controller = GitController(temp_project)
    git_controller.init_repository()
    
    # Check git setup
    assert (temp_project / ".git").exists()
    assert (temp_project / ".gitignore").exists()

def test_config_management(temp_project):
    """Test configuration handling"""
    config_handler = ConfigHandler(temp_project / ".feathers")
    
    # Test default config
    config = config_handler.get_config()
    assert "output_format" in config
    assert "auto_commit" in config
    
    # Test setting config
    config_handler.set_config("test_key", "test_value")
    config = config_handler.get_config()
    assert config["test_key"] == "test_value"

def test_query_processing():
    """Test query processing and result generation"""
    query_manager = QueryManager()
    result = query_manager.process_query("Calculate mean of column A")
    
    assert result.query == "Calculate mean of column A"
    assert isinstance(result.code, str)
    assert isinstance(result.timestamp, str)

def test_chat_session(monkeypatch, capsys):
    """Test chat session functionality"""
    # Mock user input
    inputs = iter(["help", "history", "exit"])
    monkeypatch.setattr('builtins.input', lambda prompt=None: next(inputs))
    
    # Create and run session
    session = ChatSession(auto_commit=False)
    session.start_session()
    
    # Check output
    captured = capsys.readouterr()
    assert "Welcome to Feathery ML" in captured.out
    assert "Available Commands" in captured.out

def test_banner_generation():
    """Test banner creation"""
    from rich.console import Console
    import re

    # Test creation
    banner = create_banner()
    assert isinstance(banner, Panel)
    
    # Test custom text
    custom_banner = create_banner("Test")
    assert isinstance(custom_banner, Panel)
    
    # Test content exists - look for common patterns in ASCII art
    assert "_____" in str(banner.renderable)  # Common in "Feathery" ASCII art
    assert "/_  " in str(custom_banner.renderable)  # Common in "T" ASCII art
