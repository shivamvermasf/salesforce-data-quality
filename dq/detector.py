"""Duplicate detection utilities."""

from collections import defaultdict
from typing import Any, Dict, Iterable, List, Tuple

from .rules import MatchingRule, MasterRecordRule


class DuplicateDetector:
    """Find duplicate records and select master records."""

    def __init__(self, matching_rule: MatchingRule, master_rule: MasterRecordRule) -> None:
        self.matching_rule = matching_rule
        self.master_rule = master_rule

    def group_duplicates(self, records: Iterable[Dict[str, Any]]) -> Dict[Tuple[Any, ...], List[Dict[str, Any]]]:
        """Group records by the matching rule."""
        groups: Dict[Tuple[Any, ...], List[Dict[str, Any]]] = defaultdict(list)
        for record in records:
            key = self.matching_rule.apply(record)
            groups[key].append(record)
        return {k: v for k, v in groups.items() if len(v) > 1}

    def find_duplicates(self, records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return list of duplicate groups with their master record."""
        duplicates = self.group_duplicates(records)
        results: List[Dict[str, Any]] = []
        for key, group in duplicates.items():
            master = self.master_rule.select(group)
            results.append({"match_key": key, "master": master, "duplicates": group})
        return results
