"""Command line interface for detecting duplicate Salesforce records."""

import argparse
import csv
import json
from typing import List, Dict, Any

from dq import MatchingRule, MasterRecordRule, DuplicateDetector


def load_data(path: str) -> List[Dict[str, Any]]:
    """Load account records from a CSV or JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        if path.endswith(".json"):
            return json.load(fh)
        if path.endswith(".csv"):
            reader = csv.DictReader(fh)
            return list(reader)
        raise ValueError("Unsupported file format: %s" % path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect duplicate Salesforce records")
    parser.add_argument("input", help="Path to input CSV or JSON file")
    parser.add_argument("--match-fields", nargs="+", required=True, help="Fields used to detect duplicates")
    parser.add_argument("--master-field", required=True, help="Field used to select the master record")
    parser.add_argument(
        "--strategy",
        choices=["highest", "lowest"],
        default="highest",
        help="Strategy for choosing the master record",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_data(args.input)
    matching = MatchingRule(args.match_fields)
    master_rule = (
        MasterRecordRule.highest(args.master_field)
        if args.strategy == "highest"
        else MasterRecordRule.lowest(args.master_field)
    )
    detector = DuplicateDetector(matching, master_rule)
    duplicates = detector.find_duplicates(data)

    if not duplicates:
        print("No duplicates found.")
        return

    for item in duplicates:
        print("Match key:", item["match_key"])
        print("Master record:", item["master"])
        print("Duplicates:", item["duplicates"])
        print("-")


if __name__ == "__main__":
    main()
