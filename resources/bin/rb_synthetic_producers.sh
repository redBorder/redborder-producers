#!/usr/bin/bash

# This script runs on separate screens sessions, every main producer in live directory
# To view the running screen session:
# - To watch and attach to screen: screen -r mitre_wide_attack
# - Detach from screen: Ctrl+A then D
usage() {
    echo "Usage: $0 [-s screen_name] [-f] <start|restart|stop>"
    echo
    echo "Options:"
    echo "  -s <screen_name>  Specify a single screen name to manage"
    echo "  -f               Enable fast mode (skip sleep times)"
    echo "  -h               Display this help message"
    echo
    echo "Commands:"
    echo "  start            Start the producer(s)"
    echo "  restart          Restart the producer(s)"
    echo "  stop             Stop the producer(s)"
    echo
    echo "Available screen names:"
    echo "  - traffic: produce synthetic traffic as multiple fictional exporters were producing it"
    echo "  - mitre_wide_attack: produce intrusion events like an IDS was detectecting them"
    echo "  - monitor producer usage statistics about the fictional hardware"
    echo "  - vault: produce rsyslog logs about fictional devices"
    echo "  - scanner: produce scanning events like a fictional scanner was detecting vulnerabilities in the network"
    echo
    echo "Example:"
    echo "  $0 start                     # Start all producers"
    echo "  $0 -s mitre_wide_attack start  # Start specific producer"
    
}

while getopts "hfs:" opt; do
  case $opt in
    h)
      usage
      ;;
    f)
      FAST_MODE=true
      ;;
    s)
      SCREEN_NAME="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

shift $((OPTIND-1))
ACTION=$1

if [ -z "$ACTION" ] || [[ ! "$ACTION" =~ ^(start|restart|stop)$ ]]; then
    echo "Error: First argument must be 'start', 'restart' or 'stop'" >&2
    usage
    exit 1
fi
# /usr/lib/redborder/bin/rb_synthetic_producer.rb

VALID_SCREEN_NAMES=('traffic' 'mitre_wide_attack' 'monitor' 'vault' 'scanner')
if [ -n "$SCREEN_NAME" ]; then
  SCREEN_NAMES=("$SCREEN_NAME")
else
  SCREEN_NAMES=("${VALID_SCREEN_NAMES[@]}")
fi

for SCREEN_NAME in "${VALID_SCREEN_NAMES[@]}"; do
  echo "Restarting screen instance ${SCREEN_NAME}"  
  screen -X -S ${SCREEN_NAME} quit 2>/dev/null || true # Kill screen instance if exists
  if [ "$ACTION" != "stop" ]; then
    screen -dmS ${SCREEN_NAME} python3 /usr/lib/redborder/producers/py/${SCREEN_NAME}.py #${FAST_MODE:+--fast}
  fi
  echo "Screen instance ${SCREEN_NAME} created. Watch it running screen -r ${SCREEN_NAME}"
done

screen -ls
