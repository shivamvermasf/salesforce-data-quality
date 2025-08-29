"""Data quality tools for detecting duplicate Salesforce records."""

from .rules import MatchingRule, MasterRecordRule
from .detector import DuplicateDetector

__all__ = ["MatchingRule", "MasterRecordRule", "DuplicateDetector"]
