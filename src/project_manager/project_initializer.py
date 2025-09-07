"""
Blueprint: Project Manager - Project Initializer

This module handles the creation and initialization of new statistical analysis projects.
It sets up the standard project structure and manages dependencies.

Components:
1. Project Structure Creation
2. Dependency Management (uv/pip)
3. Configuration Setup
4. Template Management
"""

from pathlib import Path
from typing import Optional, Dict, Any
import shutil
import subprocess
from dataclasses import dataclass
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class ProjectStructure:
    """Standard project structure definition"""
    project_name: str
    root_path: Path
    
    @property
    def data_dir(self) -> Path:
        return self.root_path / "data"
        
    @property
    def src_dir(self) -> Path:
        return self.root_path / "src"
        
    @property
    def config_file(self) -> Path:
        return self.root_path / ".feathers"
        
    @property
    def qna_file(self) -> Path:
        return self.root_path / "qna.json"

class ProjectInitializer:
    """Handles project initialization and setup"""
    
    def __init__(self, project_name: str, base_path: Path):
        self.structure = ProjectStructure(project_name, base_path / project_name)
        
    def create_project(self) -> Path:
        """
        Create new project with standard structure
        
        Returns:
            Path: Path to created project
        """
        try:
            self._create_directories()
            self._initialize_files()
            self._setup_dependencies()
            return self.structure.root_path
            
        except Exception as e:
            logger.error(f"Project creation failed: {str(e)}")
            raise
            
    def _create_directories(self):
        """Create project directory structure"""
        # Create main directories
        self.structure.root_path.mkdir(parents=True, exist_ok=True)
        self.structure.data_dir.mkdir(parents=True, exist_ok=True)
        self.structure.src_dir.mkdir(parents=True, exist_ok=True)
        
        # Create data subdirectories
        (self.structure.data_dir / "raw").mkdir(exist_ok=True)
        (self.structure.data_dir / "processed").mkdir(exist_ok=True)
        
    def _initialize_files(self):
        """Initialize project files"""
        # Create configuration file
        self.structure.config_file.write_text("{}")
        
        # Create QnA history file
        self.structure.qna_file.write_text("[]")
        
        # Copy requirements.txt
        shutil.copy("requirements.txt", self.structure.root_path / "requirements.txt")
        
    def _setup_dependencies(self):
        """Set up project dependencies using uv or pip"""
        try:
            if self._check_uv_available():
                self._setup_with_uv()
            else:
                self._setup_with_pip()
                
        except Exception as e:
            logger.error(f"Dependency setup failed: {str(e)}")
            raise
            
    def _check_uv_available(self) -> bool:
        """Check if uv is available"""
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            return True
        except:
            return False
            
    def _setup_with_uv(self):
        """Set up dependencies using uv"""
        subprocess.run(
            ["uv", "pip", "install", "-r", "requirements.txt"],
            cwd=self.structure.root_path,
            check=True
        )
        
    def _setup_with_pip(self):
        """Set up dependencies using pip"""
        subprocess.run(
            ["pip", "install", "-r", "requirements.txt"],
            cwd=self.structure.root_path,
            check=True
        )
