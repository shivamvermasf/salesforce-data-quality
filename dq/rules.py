"""Rule definitions for duplicate detection and master record selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Tuple


@dataclass
class MatchingRule:
    """Define fields used to identify duplicate records.

    The rule considers two records duplicates when the values of all
    specified fields match exactly.
    """

    fields: List[str]

    def apply(self, record: Dict[str, Any]) -> Tuple[Any, ...]:
        """Return a tuple key representing this record for grouping."""
        return tuple(record.get(f) for f in self.fields)


@dataclass
class MasterRecordRule:
    """Select the master record from a group of duplicates."""

    field: str
    prefer: Callable[[Any, Any], bool]

    @classmethod
    def highest(cls, field: str) -> "MasterRecordRule":
        """Select record with the highest value for ``field``."""
        return cls(field=field, prefer=lambda cur, best: cur > best)

    @classmethod
    def lowest(cls, field: str) -> "MasterRecordRule":
        """Select record with the lowest value for ``field``."""
        return cls(field=field, prefer=lambda cur, best: cur < best)

    def select(self, records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
        """Return the preferred record according to ``prefer`` function."""
        iterator = iter(records)
        try:
            best = next(iterator)
        except StopIteration:  # pragma: no cover - defensive
            raise ValueError("No records provided")
        for record in iterator:
            if self.prefer(record.get(self.field), best.get(self.field)):
                best = record
        return best
