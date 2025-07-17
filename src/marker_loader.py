import yaml
import json
from pathlib import Path
from typing import Any, Dict, List


class Marker:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get('id')
        self.level = data.get('level')
        self.name = data.get('name')
        self.atomic_pattern = data.get('atomic_pattern', [])
        self.composed_of = data.get('composed_of', [])
        self.rules = data.get('rules', [])
        self.description = data.get('description', '')


def load_marker_file(path: Path) -> Marker:
    with open(path, 'r', encoding='utf-8') as f:
        if path.suffix.lower() in {'.yaml', '.yml'}:
            data = yaml.safe_load(f)
        elif path.suffix.lower() == '.json':
            data = json.load(f)
        else:
            raise ValueError(f"Unsupported marker format: {path}")
    return Marker(data)


def load_markers(paths: List[Path]) -> List[Marker]:
    markers = []
    for p in paths:
        markers.append(load_marker_file(p))
    return markers
