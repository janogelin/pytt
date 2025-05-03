#!/bin/bash
# Extensive test script for save_parquet.py
# Covers CSV, JSON, auto-detect, invalid, empty, and overwrite cases

set -e

SCRIPT_DIR="$(dirname "$0")"
PYTHON=python3
SAVE_PARQUET="$SCRIPT_DIR/save_parquet.py"

# Test data sources
TEST_URL_CSV="https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv"
TEST_URL_JSON="https://jsonplaceholder.typicode.com/users"

# Local test data
INVALID_DATA="not,a,valid\nparquet,input"
EMPTY_DATA=""

# Output files
OUT_CSV="test_airtravel.parquet"
OUT_CSV_AUTO="test_airtravel_auto.parquet"
OUT_JSON="test_users.parquet"
OUT_JSON_AUTO="test_users_auto.parquet"
OUT_INVALID="test_invalid.parquet"
OUT_EMPTY="test_empty.parquet"
OUT_OVERWRITE="test_overwrite.parquet"

# Track failures
FAIL=0

function check_parquet() {
    local file="$1"
    local expect_rows="$2"
    local expect_cols="$3"
    if [ ! -f "$file" ]; then
        echo "  [FAIL] $file not created"
        FAIL=1
        return
    fi
    local info
    info=$($PYTHON -c "import pyarrow.parquet as pq; t = pq.read_table('$file'); print(f'Rows: {t.num_rows} Columns: {t.num_columns}')")
    echo "  [OK] $file exists. $info"
    if [ -n "$expect_rows" ] && [ -n "$expect_cols" ]; then
        local rows cols
        rows=$(echo "$info" | awk '{print $2}')
        cols=$(echo "$info" | awk '{print $4}')
        if [ "$rows" != "$expect_rows" ] || [ "$cols" != "$expect_cols" ]; then
            echo "  [FAIL] $file: Expected $expect_rows rows, $expect_cols cols, got $rows rows, $cols cols"
            FAIL=1
        fi
    fi
}

function check_fail() {
    local cmd="$1"
    if eval "$cmd"; then
        echo "  [FAIL] Command succeeded but should have failed: $cmd"
        FAIL=1
    else
        echo "  [OK] Command failed as expected: $cmd"
    fi
}

function test_csv() {
    echo "--- CSV with --format csv ---"
    rm -f "$OUT_CSV"
    curl -s "$TEST_URL_CSV" | $PYTHON "$SAVE_PARQUET" "$OUT_CSV" --format csv
    check_parquet "$OUT_CSV" 12 4
}

function test_csv_auto() {
    echo "--- CSV with auto-detect ---"
    rm -f "$OUT_CSV_AUTO"
    curl -s "$TEST_URL_CSV" | $PYTHON "$SAVE_PARQUET" "$OUT_CSV_AUTO"
    check_parquet "$OUT_CSV_AUTO" 12 4
}

function test_json() {
    echo "--- JSON with --format json ---"
    rm -f "$OUT_JSON"
    curl -s "$TEST_URL_JSON" | $PYTHON "$SAVE_PARQUET" "$OUT_JSON" --format json
    check_parquet "$OUT_JSON" 10 8
}

function test_json_auto() {
    echo "--- JSON with auto-detect ---"
    rm -f "$OUT_JSON_AUTO"
    curl -s "$TEST_URL_JSON" | $PYTHON "$SAVE_PARQUET" "$OUT_JSON_AUTO"
    check_parquet "$OUT_JSON_AUTO" 10 8
}

function test_invalid() {
    echo "--- Invalid input (should fail) ---"
    rm -f "$OUT_INVALID"
    check_fail "echo -e '$INVALID_DATA' | $PYTHON $SAVE_PARQUET $OUT_INVALID --format json"
    [ ! -f "$OUT_INVALID" ] && echo "  [OK] No file created for invalid input"
}

function test_empty() {
    echo "--- Empty input (should fail) ---"
    rm -f "$OUT_EMPTY"
    check_fail "echo -n '' | $PYTHON $SAVE_PARQUET $OUT_EMPTY --format csv"
    [ ! -f "$OUT_EMPTY" ] && echo "  [OK] No file created for empty input"
}

function test_overwrite() {
    echo "--- Overwrite existing file ---"
    rm -f "$OUT_OVERWRITE"
    # First write CSV
    curl -s "$TEST_URL_CSV" | $PYTHON "$SAVE_PARQUET" "$OUT_OVERWRITE" --format csv
    check_parquet "$OUT_OVERWRITE" 12 4
    # Overwrite with JSON
    curl -s "$TEST_URL_JSON" | $PYTHON "$SAVE_PARQUET" "$OUT_OVERWRITE" --format json
    check_parquet "$OUT_OVERWRITE" 10 8
}

function cleanup() {
    rm -f "$OUT_CSV" "$OUT_CSV_AUTO" "$OUT_JSON" "$OUT_JSON_AUTO" "$OUT_INVALID" "$OUT_EMPTY" "$OUT_OVERWRITE"
}

# Run all tests
cleanup

test_csv
test_csv_auto
test_json
test_json_auto
test_invalid
test_empty
test_overwrite

if [ "$FAIL" -eq 0 ]; then
    echo "\nAll tests PASSED."
    cleanup
    exit 0
else
    echo "\nSome tests FAILED."
    exit 1
fi 