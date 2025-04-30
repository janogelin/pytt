#!/usr/bin/env bash

# zombie_checker.sh - Zombie Process Checker
#
# This script identifies zombie processes on a Linux system and provides
# information about their parent processes for further investigation.
#
# Usage: ./zombie_checker.sh
#
# Dependencies:
#   - ps (procps-ng)
#   - awk (gawk)
#   - grep (GNU grep)

# Function to print usage information
print_usage() {
    echo "Usage: $0"
    echo "This script checks for zombie processes and their parent processes."
    exit 0
}

# Function to check dependencies
check_dependencies() {
    local dependencies=("ps" "awk" "grep")
    local missing_deps=()

    for cmd in "${dependencies[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo "Error: Missing required dependencies:"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        echo "Please install the missing dependencies and try again."
        exit 1
    fi
}

# Function to get process information
get_process_info() {
    local pid=$1
    ps -p "$pid" -o pid,ppid,user,stat,cmd --no-headers
}

# Function to check for zombie processes
check_zombies() {
    local zombie_count
    zombie_count=$(ps -A -ostat,ppid,pid,cmd | grep -e '^[Zz]' | wc -l)

    if [ "$zombie_count" -eq 0 ]; then
        echo "No zombie processes found."
        return 0
    fi

    echo "Found $zombie_count zombie process(es):"
    echo "----------------------------------------"

    # Get detailed information about zombie processes and their parents
    ps -A -ostat,ppid,pid,cmd | grep -e '^[Zz]' | while read -r line; do
        # Extract PID and PPID
        local ppid
        local pid
        ppid=$(echo "$line" | awk '{print $2}')
        pid=$(echo "$line" | awk '{print $3}')

        echo "Zombie Process:"
        echo "--------------"
        get_process_info "$pid"
        echo

        echo "Parent Process:"
        echo "--------------"
        get_process_info "$ppid"
        echo "----------------------------------------"
    done
}

# Main function
main() {
    # Check for help flag
    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        print_usage
    fi

    # Check dependencies
    check_dependencies

    # Check for zombie processes
    check_zombies
}

# Execute main function
main "$@" 