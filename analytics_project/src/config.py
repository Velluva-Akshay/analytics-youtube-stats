"""
Configuration management for YouTube Analytics.

Loads and manages configuration from YAML files.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class Config:
    """Configuration manager."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Load configuration from YAML file."""
        if config_path is None:
            # Default to config.yaml in project root
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._setup_logging()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            logging.warning(f"Config file not found: {self.config_path}. Using defaults.")
            return self._get_defaults()
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config if config else self._get_defaults()
        except Exception as e:
            logging.error(f"Error loading config: {e}. Using defaults.")
            return self._get_defaults()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            'data': {
                'csv_path': '../Global YouTube Statistics.csv',
                'encoding': 'utf-8',
                'fallback_encoding': 'latin-1'
            },
            'output': {
                'base_dir': 'outputs',
                'format': 'png',
                'dpi': 300,
                'create_subdirs': True
            },
            'visualization': {
                'style': 'seaborn-v0_8-darkgrid',
                'figure_size': [12, 6],
                'font_size': 10,
                'color_palette': 'husl',
                'save_transparent': False
            },
            'analysis': {
                'top_n': 20,
                'outlier_method': 'iqr',
                'missing_threshold': 0.5,
                'correlation_threshold': 0.7
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'analytics.log'
            }
        }
    
    def _setup_logging(self):
        """Configure logging based on config."""
        log_config = self._config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        format_str = log_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=level,
            format=format_str,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_config.get('file', 'analytics.log'))
            ]
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def get_data_config(self) -> Dict[str, Any]:
        """Get data configuration."""
        return self._config.get('data', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output configuration."""
        return self._config.get('output', {})
    
    def get_viz_config(self) -> Dict[str, Any]:
        """Get visualization configuration."""
        return self._config.get('visualization', {})
    
    def get_analysis_config(self) -> Dict[str, Any]:
        """Get analysis configuration."""
        return self._config.get('analysis', {})


# Global config instance
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create global config instance."""
    global _config_instance
    
    if _config_instance is None or config_path is not None:
        _config_instance = Config(config_path)
    
    return _config_instance
