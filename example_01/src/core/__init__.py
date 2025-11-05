"""Core utilities and shared functionality."""

from pathlib import Path
from .config import Config

# Create a configured instance
config = Config(config_path=Path(__file__).parent.parent.parent / "config.yaml")

# Export the configured instance
__all__ = ["config"]