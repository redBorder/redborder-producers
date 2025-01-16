#!/bin/bash

# This script runs on separate screens sessions, every main producer in live directory
# To view the running screen session:
# - To watch and attach to screen: screen -r mitre_wide_attack
# - Detach from screen: Ctrl+A then D


while getopts "hfs:" opt; do
  case $opt in
    h)
      # echo "Usage: $0 [-s screen_name] [-f --fast]"
      # # echo "Starts the mitre_wide_attack.py script in a screen session"

      # Starts the mitre_wide_attack.py script in a screen session
      # echo "-f: enable fast attack mode, to jump sleep times"
      # python3 mitre_wide_attack.py -h
      exit 0
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
  screen -dmS ${SCREEN_NAME} python3 /usr/lib/redborder/producers/${SCREEN_NAME}.py #${FAST_MODE:+--fast}
done

echo "Screen instance ${SCREEN_NAME} created. Watch it running screen -r ${SCREEN_NAME}"
