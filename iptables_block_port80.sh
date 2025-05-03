#!/usr/bin/env bash

# iptables_block_port.sh
#
# This script blocks all incoming traffic on a specified TCP port (default: 80) using iptables.
# Requires root privileges.

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root." >&2
  exit 1
fi

# Get port from argument or default to 80
PORT=${1:-80}

# Block incoming TCP traffic on the specified port
iptables -A INPUT -p tcp --dport "$PORT" -j DROP

# Show the rule just added
echo "Current iptables rules for port $PORT:"
iptables -L INPUT -n --line-numbers | grep ":$PORT"

echo "Incoming TCP traffic on port $PORT is now blocked."

echo
# Print all iptables rules
echo "All current iptables rules:"
iptables -L -n --line-numbers 