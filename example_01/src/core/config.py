"""Configuration management for MLOps project.

This module provides a flexible configuration system that can load settings
from various sources (YAML files, environment variables, etc.) and supports
different types of configurations (MLflow, database, etc.).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import os
import yaml


@dataclass
class BaseConfig:
    """Base configuration class with common functionality."""
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'BaseConfig':
        """Create config from YAML file."""
        if not yaml_path.exists():
            raise FileNotFoundError(f"Config file not found: {yaml_path}")
            
        with yaml_path.open("r") as f:
            config_dict = yaml.safe_load(f)
            return cls(**config_dict)
    
    @classmethod
    def from_env(cls, prefix: str = "") -> 'BaseConfig':
        """Create config from environment variables.
        
        Args:
            prefix: Prefix for env variables (e.g., 'MLFLOW_' for MLFLOW_TRACKING_URI)
        """
        config_dict = {}
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            # Remove prefix and convert to lowercase for config
            clean_key = key[len(prefix):].lower() if prefix else key.lower()
            config_dict[clean_key] = value
        return cls(**config_dict)


@dataclass
class MLflowConfig(BaseConfig):
    """MLflow specific configuration."""
    tracking_uri: str = "http://localhost:5000"
    experiment_name: Optional[str] = None
    artifact_location: Optional[str] = None

    @classmethod
    def default(cls) -> 'MLflowConfig':
        """Create default MLflow configuration."""
        return cls()


@dataclass
class DatabaseConfig(BaseConfig):
    """Database configuration."""
    host: str = "localhost"
    port: int = 3306
    database: str = "mlflowdb"
    username: str = "root"
    password: Optional[str] = None

    @property
    def uri(self) -> str:
        """Get database URI."""
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class Config:
    """Main configuration class that manages all config types."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        env_prefix: str = "",
    ):
        self.mlflow = MLflowConfig.default()
        self.database = DatabaseConfig()
        
        if config_path and config_path.exists():
            self.load_yaml(config_path)
        
        if env_prefix:
            self.load_env(env_prefix)
    
    def load_yaml(self, config_path: Path) -> None:
        """Load configuration from YAML file."""
        with config_path.open("r") as f:
            config_dict = yaml.safe_load(f)
            
        if "mlflow" in config_dict:
            self.mlflow = MLflowConfig(**config_dict["mlflow"])
        if "database" in config_dict:
            self.database = DatabaseConfig(**config_dict["database"])
    
    def load_env(self, prefix: str = "") -> None:
        """Load configuration from environment variables."""
        self.mlflow = MLflowConfig.from_env(f"{prefix}MLFLOW_")
        self.database = DatabaseConfig.from_env(f"{prefix}DB_")


# Example usage:
if __name__ == "__main__":
    # Load from YAML
    config = Config(Path("config.yaml"))
    
    # Or use environment variables
    # export MLFLOW_TRACKING_URI=http://localhost:5000
    # config = Config(env_prefix="MY_APP_")
    
    # Access configurations
    mlflow_uri = config.mlflow.tracking_uri
    db_uri = config.database.uri
