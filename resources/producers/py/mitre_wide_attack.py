#!/usr/bin/python3
from producer import period_producer
import argparse
def usage():
  '''
  This script is used to run different incidentes that are following a full path of Mitre tactics, by running the corresponding scripts.
  Each of the scripts is responsible for running the incident that triggers the corresponding tactic.
  The orden is left to right, corresponding on the column order of the orginal mitre matrix
  On start, this script will create an instace in screen named "mitre_wide_attack" and will repeat itself every 1 hour. So.
  At start it will simulate multiple events of the detection of the first mitre tactic: a recognition phase.
  After 1/13 hours, it will simulate the second tactic, and so on.
  At the end of the loop, it will print what's the next time the script will restart the loop again.
  '''
  print(__doc__)
  exit()

# Array of scripts to execute in sequence
SCRIPTS_PATH = [
  # Add paths to your attack scripts here, one per line
  '/usr/lib/redborder/producers/py/at1_reconocimiento_scan.py',
  '/usr/lib/redborder/producers/py/at2_resource_development_ssl.py',
  '/usr/lib/redborder/producers/py/at3.py',
  '/usr/lib/redborder/producers/py/at5_persistence_backdoor.py',
  '/usr/lib/redborder/producers/py/at6.py',
  '/usr/lib/redborder/producers/py/at7_defense_evasion.py',
  '/usr/lib/redborder/producers/py/at8_credential_access.py',
  '/usr/lib/redborder/producers/py/at9_discovery.py',
  '/usr/lib/redborder/producers/py/at10_lateral_movement.py',
  '/usr/lib/redborder/producers/py/at11_collection_screen.py',
  '/usr/lib/redborder/producers/py/at12_cnc.py',
  '/usr/lib/redborder/producers/py/at13_exfiltration_dropbox.py',
  '/usr/lib/redborder/producers/py/at14_impact_ransom.py'
]
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('-f', '--fast', action='store_true', default=False, help='Run with no wait between incidents')
  parser.add_argument('-l', '--looptime', default=3600, help='Time in seconds to start again the tactics happening')

  args = parser.parse_args()    
  period_producer(SCRIPTS_PATH, args.looptime, args.fast)
