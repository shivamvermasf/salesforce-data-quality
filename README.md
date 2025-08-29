# Salesforce Data Quality

This repository contains a simple command-line application that helps
identify duplicate Salesforce account (or related object) records.

## Features

- **Matching rules** – choose which fields must match for records to be
  considered duplicates.
- **Master record selection** – choose a field and strategy (highest or
  lowest) to determine which record should remain as the master.

## Usage

```bash
python cli.py sample_accounts.csv --match-fields Name Email \
  --master-field LastModifiedDate --strategy highest
```

The example above groups records that share the same `Name` and `Email`
and selects the record with the most recent `LastModifiedDate` as the
master.

Sample data is provided in `sample_accounts.csv`.

