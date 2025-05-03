#!/usr/bin/env bash

# iptables_block_port80.sh
#
# This script blocks all incoming traffic on TCP port 80 (HTTP) using iptables.
# Requires root privileges.

# Check for root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root." >&2
  exit 1
fi

# Block incoming TCP traffic on port 80
iptables -A INPUT -p tcp --dport 80 -j DROP

# Show the rule just added
echo "Current iptables rules for port 80:" 
iptables -L INPUT -n --line-numbers | grep ':80'

echo "Incoming TCP traffic on port 80 is now blocked."

echo
# Print all iptables rules
echo "All current iptables rules:"
iptables -L -n --line-numbers 