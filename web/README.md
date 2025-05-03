# save_parquet.py

A robust utility to save data received from `curl` (or any stdin) as a Parquet file. Supports CSV and JSON input, auto-detection, error handling, and is accompanied by an extensive test suite.

## Features
- Accepts CSV or JSON data from stdin (e.g., via `curl` or pipes)
- Auto-detects input format if not specified
- Saves data as an efficient Parquet file using `pyarrow`
- Handles errors gracefully (invalid/empty input, parse errors)
- Overwrites output files if they exist
- Provides clear command-line feedback
- Extensively tested for correctness and edge cases

## Usage

```sh
curl <url> | python3 save_parquet.py output.parquet [--format csv|json]
```

- `output.parquet`: Path to the output Parquet file.
- `--format`: (Optional) Specify `csv` or `json`. If omitted, the script tries to auto-detect the format based on the input.

### Examples

Save CSV data:
```sh
curl https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv | python3 save_parquet.py data.parquet --format csv
```

Save JSON data:
```sh
curl https://jsonplaceholder.typicode.com/users | python3 save_parquet.py data.parquet --format json
```

Auto-detect format:
```sh
curl https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv | python3 save_parquet.py data.parquet
```

### Error Handling
- If no data is received on stdin, the script prints an error and exits nonzero.
- If the input cannot be parsed as the specified or detected format, an error is printed and no file is created.
- If the output file already exists, it is overwritten.

### Output
- On success, prints the number of rows saved and the output file name.
- On failure, prints a clear error message to stderr and exits with a nonzero code.

## Requirements
- Python 3
- `pandas` and `pyarrow` (install with `pip install -r requirements.txt`)

## Testing & Coverage

An extensive test suite is provided in `test_save_parquet.sh`:
- Tests CSV and JSON input (with and without `--format`)
- Tests auto-detection of format
- Tests invalid and empty input (should fail and not create a file)
- Tests overwriting an existing file
- Verifies row and column counts for each output
- Prints clear PASS/FAIL for each test and a summary

### Run all tests:
```sh
bash web/test_save_parquet.sh
```

Example output:
```
--- CSV with --format csv ---
  [OK] test_airtravel.parquet exists. Rows: 12 Columns: 4
--- CSV with auto-detect ---
  [OK] test_airtravel_auto.parquet exists. Rows: 12 Columns: 4
--- JSON with --format json ---
  [OK] test_users.parquet exists. Rows: 10 Columns: 8
--- JSON with auto-detect ---
  [OK] test_users_auto.parquet exists. Rows: 10 Columns: 8
--- Invalid input (should fail) ---
  [OK] Command failed as expected: echo -e 'not,a,valid\nparquet,input' | python3 web/save_parquet.py test_invalid.parquet --format json
  [OK] No file created for invalid input
--- Empty input (should fail) ---
  [OK] Command failed as expected: echo -n '' | python3 web/save_parquet.py test_empty.parquet --format csv
  [OK] No file created for empty input
--- Overwrite existing file ---
  [OK] test_overwrite.parquet exists. Rows: 12 Columns: 4
  [OK] test_overwrite.parquet exists. Rows: 10 Columns: 8

All tests PASSED.
```

## Security & Performance Notes
- The script reads all input into memory before processing; for very large files, consider chunked processing.
- Only use this utility with trusted data sources, as malformed or malicious input could cause resource exhaustion or unexpected behavior.
- Output files are overwritten without prompt.

## Troubleshooting
- If you see `ModuleNotFoundError`, ensure you have installed all requirements:
  ```sh
  pip install -r requirements.txt
  ```
- If a test fails, check the error message for details. Network issues may affect tests that fetch remote data.

## Contribution
- Contributions and suggestions are welcome! Please ensure new features are covered by tests.
- For bug reports, include the command used, input data, and error output.

---

**Author:** [Your Name or Organization]

**License:** MIT (or specify your license)

## Parallel Web Crawler (`crawler.py`)

A simple Python web crawler that reads a list of URIs from a file, spawns 5 independent processes, fetches each URI, and outputs the results in a Parquet file (compatible with `save_parquet.py`).

### Usage

```sh
python3 crawler.py uris.txt output.parquet
```
- `uris.txt`: Text file with one URI per line
- `output.parquet`: Output Parquet file with crawl results

### Output Columns
- `url`: The URI fetched
- `status_code`: HTTP status code (or None on error)
- `content_length`: Length of the response content (0 on error)
- `snippet`: First 200 characters of the response (or error message)

### Features
- Spawns 5 independent processes for parallel crawling
- Handles timeouts and errors gracefully
- Skips blank lines in the input file
- Output is a Parquet file for easy analysis

### Requirements
- `requests` (install with `pip install -r requirements.txt`)

### Example

```
$ cat uris.txt
https://www.example.com
https://www.python.org
https://notarealwebsite.abc

$ python3 crawler.py uris.txt crawl_results.parquet
Crawled 3 URLs. Results saved to crawl_results.parquet
```

---

## Automated Testing & Coverage for `crawler.py`

Automated tests for the crawler are provided in `test_crawler.py` using `pytest` and `unittest.mock`.

### Running the Tests

From the project root:
```sh
pytest web/test_crawler.py
```

### Test Coverage
To check test coverage (requires `pytest-cov`):
```sh
pip install pytest-cov
pytest --cov=web web/test_crawler.py
```

### What is Tested?
- Normal crawl with mocked HTTP responses (success and failure)
- Empty input file (should exit with error)
- Invalid URL (simulated request exception)
- Output file correctness (row content, error handling)

All network requests are mocked for reliability and speed.

--- 