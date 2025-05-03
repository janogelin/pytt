#!/usr/bin/env python3
"""
Save stdin data (CSV or JSON) to a Parquet file.
Usage:
    curl ... | python3 save_parquet.py output.parquet [--format csv|json]

If --format is not specified, tries to auto-detect from input.
"""
import sys
import argparse
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import io


def main():
    parser = argparse.ArgumentParser(description="Save stdin data (CSV or JSON) to a Parquet file.")
    parser.add_argument("output", help="Output Parquet file path")
    parser.add_argument("--format", choices=["csv", "json"], help="Input format (csv or json). If omitted, auto-detect.")
    args = parser.parse_args()

    # Read all stdin
    raw = sys.stdin.read()
    if not raw.strip():
        print("Error: No input data received on stdin.", file=sys.stderr)
        sys.exit(1)

    fmt = args.format
    df = None
    # Try to auto-detect if not specified
    if not fmt:
        if raw.lstrip().startswith("{") or raw.lstrip().startswith("["):
            fmt = "json"
        else:
            fmt = "csv"

    try:
        if fmt == "csv":
            df = pd.read_csv(io.StringIO(raw))
        elif fmt == "json":
            df = pd.read_json(io.StringIO(raw))
        else:
            print(f"Unknown format: {fmt}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing input as {fmt}: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        table = pa.Table.from_pandas(df)
        pq.write_table(table, args.output)
        print(f"Saved {len(df)} rows to {args.output}")
    except Exception as e:
        print(f"Error writing Parquet file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 