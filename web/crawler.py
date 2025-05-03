#!/usr/bin/env python3
"""
Simple parallel web crawler.

Usage:
    python3 crawler.py uris.txt output.parquet

- uris.txt: File with one URI per line
- output.parquet: Output Parquet file (same format as save_parquet.py)

Spawns 5 independent processes to fetch URLs in parallel.
"""
import sys
import argparse
import multiprocessing as mp
import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# For testability, allow pool and fetch_fn injection
def fetch_url(url):
    url = url.strip()
    if not url:
        return None
    try:
        resp = requests.get(url, timeout=10)
        return {
            'url': url,
            'status_code': resp.status_code,
            'content_length': len(resp.content),
            'snippet': resp.text[:200] if resp.ok else '',
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': None,
            'content_length': 0,
            'snippet': f'ERROR: {e}',
        }

def crawl(uris, output, pool_cls=mp.Pool, fetch_fn=fetch_url, pool_size=5):
    if not uris:
        print("No URIs found in input file.", file=sys.stderr)
        sys.exit(1)
    with pool_cls(pool_size) as pool:
        results = list(pool.imap_unordered(fetch_fn, uris))
    results = [r for r in results if r]
    if not results:
        print("No results to write.", file=sys.stderr)
        sys.exit(1)
    df = pd.DataFrame(results)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, output)
    print(f"Crawled {len(results)} URLs. Results saved to {output}")

def main():
    parser = argparse.ArgumentParser(description="Simple parallel web crawler.")
    parser.add_argument("input", help="Input file with URIs (one per line)")
    parser.add_argument("output", help="Output Parquet file")
    args = parser.parse_args()
    with open(args.input) as f:
        uris = [line.strip() for line in f if line.strip()]
    crawl(uris, args.output)

if __name__ == "__main__":
    main() 