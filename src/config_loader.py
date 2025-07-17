import yaml
import json
from pathlib import Path
from typing import Any, Dict


def load_schema(path: Path) -> Dict[str, Any]:
    """Load a schema definition from YAML or JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        if path.suffix.lower() in {'.yaml', '.yml'}:
            return yaml.safe_load(f)
        elif path.suffix.lower() == '.json':
            return json.load(f)
        else:
            raise ValueError(f"Unsupported schema format: {path}")
