"""
Blueprint: Configuration Manager - Config Handler

This module manages project configuration, including settings storage,
retrieval, and validation.

Components:
1. Configuration Storage
2. Settings Management
3. Validation Rules
4. Default Settings
"""

from pathlib import Path
from typing import Dict, Any, Optional
import json
from dataclasses import dataclass
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class ConfigDefaults:
    """Default configuration settings"""
    output_format: str = "text"
    auto_commit: bool = True
    save_history: bool = True

class ConfigHandler:
    """Handles project configuration management"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.cwd() / ".feathers"
        self.defaults = ConfigDefaults()
        
    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration
        
        Returns:
            Dict[str, Any]: Current configuration
        """
        try:
            if self.config_path.exists():
                config = json.loads(self.config_path.read_text())
                if not config:  # Empty config file
                    config = self._create_default_config()
                    self._save_config(config)
                return config
            else:
                config = self._create_default_config()
                self._save_config(config)
                return config
            
        except Exception as e:
            logger.error(f"Failed to read configuration: {str(e)}")
            raise
            
    def set_config(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        try:
            config = self.get_config()
            config[key] = value
            self._save_config(config)
            logger.info(f"Updated configuration: {key}={value}")
            
        except Exception as e:
            logger.error(f"Failed to set configuration: {str(e)}")
            raise
            
    def reset_config(self) -> None:
        """Reset configuration to defaults"""
        try:
            self._save_config(self._create_default_config())
            logger.info("Reset configuration to defaults")
            
        except Exception as e:
            logger.error(f"Failed to reset configuration: {str(e)}")
            raise
            
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        return {
            "output_format": self.defaults.output_format,
            "auto_commit": self.defaults.auto_commit,
            "save_history": self.defaults.save_history
        }
        
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file"""
        self.config_path.write_text(json.dumps(config, indent=2))
