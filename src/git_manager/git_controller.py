"""
Blueprint: Git Manager - Git Controller

This module handles all git-related operations for the project, including
initialization, commits, and remote operations.

Components:
1. Repository Management
2. Change Tracking
3. Remote Operations
4. Branch Management
"""

from pathlib import Path
from typing import Optional, List
import subprocess
from dataclasses import dataclass
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class GitConfig:
    """Git configuration settings"""
    repo_path: Path
    remote_url: Optional[str] = None

class GitController:
    """Handles git operations"""
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        
    def init_repository(self) -> None:
        """Initialize a new git repository"""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.repo_path,
                check=True
            )
            self._create_gitignore()
            logger.info(f"Initialized git repository at {self.repo_path}")
            
        except Exception as e:
            logger.error(f"Git initialization failed: {str(e)}")
            raise
            
    def commit_changes(self, message: Optional[str] = None) -> None:
        """
        Commit changes to repository
        
        Args:
            message: Commit message (auto-generated if None)
        """
        try:
            # Stage changes
            subprocess.run(
                ["git", "add", "."],
                cwd=self.repo_path,
                check=True
            )
            
            # Create commit
            msg = message or "Update: Analysis results"
            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=self.repo_path,
                check=True
            )
            
            logger.info(f"Committed changes: {msg}")
            
        except Exception as e:
            logger.error(f"Git commit failed: {str(e)}")
            raise
            
    def push_changes(self) -> None:
        """Push changes to remote repository"""
        try:
            subprocess.run(
                ["git", "push"],
                cwd=self.repo_path,
                check=True
            )
            logger.info("Pushed changes to remote")
            
        except Exception as e:
            logger.error(f"Git push failed: {str(e)}")
            raise
            
    def _create_gitignore(self) -> None:
        """Create .gitignore file with standard entries"""
        gitignore_content = """
        # Python
        __pycache__/
        *.py[cod]
        *$py.class
        *.so
        .Python
        env/
        build/
        develop-eggs/
        dist/
        downloads/
        eggs/
        .eggs/
        lib/
        lib64/
        parts/
        sdist/
        var/
        wheels/
        *.egg-info/
        .installed.cfg
        *.egg

        # Virtual Environment
        venv/
        ENV/

        # IDE
        .idea/
        .vscode/
        *.swp
        *.swo

        # Project specific
        data/raw/
        data/processed/
        """
        
        gitignore_path = self.repo_path / ".gitignore"
        gitignore_path.write_text(gitignore_content)
