import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .marker_loader import Marker


@dataclass
class MarkerMatch:
    marker_id: str
    start: int
    end: int
    level: int


class MarkerEngine:
    def __init__(self, schema: Dict[str, Any], markers: List[Marker]):
        self.schema = schema
        self.markers = markers
        self.atomic_markers = [m for m in markers if m.level == 1]
        self.semantic_markers = [m for m in markers if m.level == 2]

    def normalize_text(self, text: str) -> str:
        return text.lower()

    def tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def atomic_scan(self, text: str) -> List[MarkerMatch]:
        matches = []
        for marker in self.atomic_markers:
            for pattern in marker.atomic_pattern:
                for m in re.finditer(pattern, text, re.IGNORECASE):
                    matches.append(MarkerMatch(marker.id, m.start(), m.end(), marker.level))
        return matches

    def evaluate_semantic(self, atomic_matches: List[MarkerMatch]) -> List[MarkerMatch]:
        results = []
        atomic_ids = [m.marker_id for m in atomic_matches]
        for marker in self.semantic_markers:
            satisfied = True
            for rule in marker.rules:
                if rule.get('type') == 'frequency':
                    count = atomic_ids.count(rule['marker'])
                    if count < rule.get('min', 1):
                        satisfied = False
                        break
            if satisfied:
                results.append(MarkerMatch(marker.id, 0, 0, marker.level))
        return results

    def run(self, text: str) -> Dict[str, Any]:
        normalized = self.normalize_text(text)
        atomic_matches = self.atomic_scan(normalized)
        semantic_matches = self.evaluate_semantic(atomic_matches)
        return {
            'text': text,
            'atomic_matches': [m.__dict__ for m in atomic_matches],
            'semantic_matches': [m.__dict__ for m in semantic_matches],
        }
