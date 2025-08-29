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
    parser.add_argument("input", nargs="?", help="Path to input CSV or JSON file")
    parser.add_argument("--match-fields", nargs="+", help="Fields used to detect duplicates")
    parser.add_argument("--master-field", help="Field used to select the master record")
    parser.add_argument(
        "--strategy",
        choices=["highest", "lowest"],
        default="highest",
        help="Strategy for choosing the master record",
    )
    parser.add_argument(
        "--config",
        help="Path to JSON config defining multiple rule sets",
    )
    args = parser.parse_args()
    if not args.config:
        if not (args.input and args.match_fields and args.master_field):
            parser.error(
                "input, --match-fields and --master-field are required unless --config is provided"
            )
    return args


def run_detector(data: List[Dict[str, Any]], match_fields: List[str], master_field: str, strategy: str) -> None:
    """Run duplicate detection and print results."""
    matching = MatchingRule(match_fields)
    master_rule = (
        MasterRecordRule.highest(master_field)
        if strategy == "highest"
        else MasterRecordRule.lowest(master_field)
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


def main() -> None:
    args = parse_args()
    if args.config:
        config = json.load(open(args.config, "r", encoding="utf-8"))
        for rule in config.get("rules", []):
            print("Object:", rule.get("object", ""))
            data = load_data(rule["input"])
            run_detector(
                data,
                rule["match_fields"],
                rule["master_field"],
                rule.get("strategy", "highest"),
            )
    else:
        data = load_data(args.input)
        run_detector(data, args.match_fields, args.master_field, args.strategy)


if __name__ == "__main__":
    main()
