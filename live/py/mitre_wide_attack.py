#!/usr/bin/env python3

def usage():
    '''
    This script is used to run different incidentes that are following a full path of Mitre tactics, by running the corresponding scripts.
    Each of the scripts is responsible for running the incident that triggers the corresponding tactic.
    The orden is left to right, corresponding on the column order of the orginal mitre matrix
    On start, this script will create an instace in screen named "mitre_wide_attack" and will repeat itself every 2 hours.
    '''
    print(__doc__)
    exit()

# Array of scripts to execute in sequence
SCRIPTS_PATH = [
    # Add paths to your attack scripts here, one per line
    '/usr/lib/redborder/producers/live/attacks/at1_reconocimiento_scan.py',
    '/usr/lib/redborder/producers/live/attacks/at2_resource_development_ssl.py',
    '/usr/lib/redborder/producers/live/attacks/at3.py',
    '/etc/synthetic_producer/config/vault_new_powershell.yml',
    '/usr/lib/redborder/producers/live/attacks/at5_persistence_backdoor.py',
    '/usr/lib/redborder/producers/live/attacks/at6.py',
    '/usr/lib/redborder/producers/live/attacks/at7_defense_evasion.py',
    '/usr/lib/redborder/producers/live/attacks/at8_credential_access.py',
    '/usr/lib/redborder/producers/live/attacks/at9_lateral_movement.py',
    '/usr/lib/redborder/producers/live/attacks/at9_discovery.py',
    '/usr/lib/redborder/producers/live/attacks/at10_collection_screen.py',
    '/usr/lib/redborder/producers/live/attacks/at11_exfiltration_dropbox.py',
    '/usr/lib/redborder/producers/live/attacks/at12_cnc.py',
    '/usr/lib/redborder/producers/live/attacks/at13_impact_ransom.py'
]

import os
import time
from datetime import datetime, timedelta
import argparse

TEST_TIME=10
TIME_TO_NEXT_ATTACK=600
def check_and_kill_process(script, command):
    os.system(f'pkill -f "{command}"')
    time.sleep(5)
    check_process = os.popen(f'pgrep -f "{command}"').read()
    while check_process:
        os.system('figlet "WARNING: Process still running"')
        print(f"Warning: Process for {script} is still running")
        os.system(f'pkill -f "{command}"')
        time.sleep(5)
        check_process = os.popen(f'pgrep -f "{command}"').read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', '--fast', action='store_true', default=False, help='Run with no wait between incidents')
    parser.add_argument('-l', '--looptime', default=3600, help='Time in seconds to start again the tactics happening')

    args = parser.parse_args()    

    while True:
        for script in SCRIPTS_PATH:
            print('Starting attack script')
            os.system(f'figlet "{os.path.basename(script)}"')   
            if not os.path.exists(script):
                print(f"ERROR: Script {script} not found")
                continue
            if script.endswith('.yml'):
                command = f'rb_synthetic_producer -r 1 -p 1 -c {script}'
                os.system(f'{command} &')
                time.sleep(10) # because synthetic needs more time to start
                check_and_kill_process(script, command)
            else:
                command = f'python3 {script}'
                os.system(command)
                time.sleep(5)
                check_and_kill_process(script, command)
        time.sleep(TEST_TIME if args.fast else TIME_TO_NEXT_ATTACK)        
        next_run_str = datetime.now() + timedelta(hours=args.looptime/3600)
        os.system(f'figlet "Repeating scenario at {next_run_str.strftime("%H:%M")} UTC"')
        time.sleep(args.looptime)