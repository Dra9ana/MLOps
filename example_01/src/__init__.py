"""example_01 package"""

__version__ = "0.0.1"

from pathlib import Path
from .core.config import Config

# Initialize config with project root path
project_root = Path(__file__).parent.parent.parent
config = Config(project_root / "config.yaml")

# Export config for easy access
__all__ = ["config"]
