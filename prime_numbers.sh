#!/usr/bin/env bash

# prime_numbers.sh
#
# This script calculates and prints all prime numbers up to a given limit.
# Usage: ./prime_numbers.sh <limit>

# Check for argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <limit>"
  exit 1
fi

LIMIT=$1

# Validate input is a positive integer
if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [ "$LIMIT" -lt 2 ]; then
  echo "Please provide a positive integer >= 2."
  exit 1
fi

# Function to check if a number is prime
is_prime() {
  local n=$1
  if [ "$n" -le 3 ]; then
    [ "$n" -ge 2 ] && return 0 || return 1
  fi
  if [ $((n % 2)) -eq 0 ] || [ $((n % 3)) -eq 0 ]; then
    return 1
  fi
  local i=5
  while [ $((i * i)) -le "$n" ]; do
    if [ $((n % i)) -eq 0 ] || [ $((n % (i + 2))) -eq 0 ]; then
      return 1
    fi
    i=$((i + 6))
  done
  return 0
}

# Print all primes up to LIMIT
for ((num=2; num<=LIMIT; num++)); do
  if is_prime "$num"; then
    echo "$num"
  fi
done 