# Salesforce Data Quality

This repository contains tools that help identify duplicate Salesforce account (or related object) records.

## Features

- **Matching rules** – choose which fields must match for records to be considered duplicates.
- **Master record selection** – choose a field and strategy (highest or lowest) to determine which record should remain as the master.
- **Command-line interface** – run duplicate checks over a data file.
- **Web UI** – upload data and experiment with rules in the browser.

## Installation

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
python cli.py sample_accounts.csv --match-fields Name Email \
  --master-field LastModifiedDate --strategy highest
```

The example above groups records that share the same `Name` and `Email` and selects the record with the most recent `LastModifiedDate` as the master.

Sample data is provided in `sample_accounts.csv`.

## Web UI

```bash
python web.py
```

Open http://localhost:5000 and upload a CSV or JSON file. Enter the fields to match, the master field and a strategy to view detected duplicates.
