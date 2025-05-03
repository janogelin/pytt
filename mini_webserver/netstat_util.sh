#!/usr/bin/env bash
# netstat_util.sh - Simple utility to run common netstat commands

set -e

usage() {
    echo "Usage: $0 [option] [port]"
    echo "Options:"
    echo "  1   netstat -a   (all sockets)"
    echo "  2   netstat -at  (all TCP sockets)"
    echo "  3   netstat -l   (listening sockets)"
    echo "  4   netstat -lx  (listening UNIX sockets)"
    echo "  5   netstat -s   (statistics)"
    echo "  6   netstat -an | grep :<port>   (info for specific port, requires port as 2nd argument)"
    echo "  h   Show this help message"
    exit 1
}

if [[ $# -eq 0 ]]; then
    usage
fi

case "$1" in
    1)
        echo "> netstat -a"
        netstat -a
        ;;
    2)
        echo "> netstat -at"
        netstat -at
        ;;
    3)
        echo "> netstat -l"
        netstat -l
        ;;
    4)
        echo "> netstat -lx"
        netstat -lx
        ;;
    5)
        echo "> netstat -s"
        netstat -s
        ;;
    6)
        #n numeric busy machine flag
        if [[ -z "$2" ]]; then
            echo "> netstat -an (no port specified)"
            netstat -an
        else
            echo "> netstat -an | grep :$2"
            netstat -an | grep ":$2"
        fi
        ;;
    h|--help|-h)
        usage
        ;;
    *)
        echo "Unknown option: $1"
        usage
        ;;
esac 