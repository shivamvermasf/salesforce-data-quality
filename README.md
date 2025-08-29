# Salesforce Data Quality

This repository contains tools that help identify duplicate Salesforce account (or related object) records.

## Features

- **Matching rules** – choose which fields must match for records to be considered duplicates.
- **Master record selection** – choose a field and strategy (highest or lowest) to determine which record should remain as the master.
- **Command-line interface** – run duplicate checks over a data file.
- **Web UI** – React + Redux front end to upload data and experiment with rules in the browser.

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

Sample account data is provided in `sample_accounts.csv`. A contacts example lives in `sample_contacts.csv`.

You can also run multiple rule sets in one go using a JSON config:

```bash
python cli.py --config rules.json
```

Each entry in `rules.json` specifies the object, input file, matching fields, master field and strategy.

## Web UI

```bash
python web.py
```

Open http://localhost:5000 to access the React app. Upload a CSV or JSON file, enter match fields, choose the master field and strategy to view detected duplicates.
