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
    echo "  - traffic_namespace"
    echo "  - traffic_with_sense"
    echo "  - mitre_wide_attack"
    echo "  - monitor_routers"
    echo "  - vault"
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

if [ -z "${SCREEN_NAME}" ]; then
  SCREEN_NAMES=("mitre_wide_attack" "vault")
  SCREEN_NAMES=("traffic_namespace" "traffic_with_sense" "mitre_wide_attack" "monitor_routers" "vault")
else
  SCREEN_NAMES=("${SCREEN_NAME}")
fi

for SCREEN_NAME in "${SCREEN_NAMES[@]}"; do
  echo "Restarting screen instance ${SCREEN_NAME}"  
  screen -X -S ${SCREEN_NAME} quit 2>/dev/null || true # Kill screen instance if exists
  if [ "$ACTION" != "stop" ]; then
    screen -dmS ${SCREEN_NAME} python3 /usr/lib/redborder/producers/${SCREEN_NAME}.py #${FAST_MODE:+--fast}
  fi
done

echo "Screen instance ${SCREEN_NAME} created. Watch it running screen -r ${SCREEN_NAME}"
