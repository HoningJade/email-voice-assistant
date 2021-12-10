import argparse
import os
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true",
                    help="Whether to run in debug mode.")
args = parser.parse_args()
DEBUG = args.debug

# flask
dir_name = os.path.dirname(__file__)
drivers = ["nlp", "backend"]
process = {}

for d in drivers:
    driver_name = "debug_" + d if DEBUG else "run_" + d
    driver_path = os.path.join(dir_name, driver_name)
    process[d] = subprocess.Popen([driver_path])

# yarn
os.chdir("frontend")
process["frontend"] = subprocess.Popen(["yarn", "start"], stdout=open("frontend.log", mode="w"))
os.chdir("..")

while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        for k, v in process.items():
            v.terminate()
            print(k + " has been killed.")
        exit(0)

