import os
import sys
import time
import shlex
import subprocess


def run_cmd(cmd):
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, env=os.environ)
    proc.communicate()


ROOT_DIR = os.path.join(os.path.dirname(__file__), "..", "..")

name = sys.argv[1]
if len(sys.argv) > 2:
    BIN_DIR = sys.argv[2]
else:
    BIN_DIR = os.path.join(ROOT_DIR, "bin")

# start stack
curdir = os.getcwd()
os.chdir(os.path.join(ROOT_DIR, "connectors", "sources", "tests", "fixtures", name))

#run_cmd("make run-stack")

# XXX make run-stack should be blocking until everythign is up and running by checking hbs
#time.sleep(30)

#run_cmd("docker ps -a")
#time.sleep(240)
run_cmd(
    f"{BIN_DIR}/fake-kibana --index-name search-{name} --service-type {name} --debug"
)
run_cmd(f"{BIN_DIR}/elastic-ingest --one-sync --sync-now")
run_cmd(f"{BIN_DIR}/elastic-ingest --one-sync --sync-now")
run_cmd(
    f"{BIN_DIR}/python {ROOT_DIR}/scripts/verify.py --index-name search-{name} --service-type {name} --size 3000"
)
