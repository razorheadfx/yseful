#!/usr/bin/python
#this works with python2 and 3

import sys
import os
import subprocess
import signal

"""
set the cpu governor of all cores to the provided value
"""

def sigint_handler(signal, stackframe):
    print("Exiting on user interrupt")
    sys.exit(130)

def cpufreq_set_installed():
    p = subprocess.Popen(["/usr/bin/which","cpufreq-set"], stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return False
    else:
        return True

def get_available_governors():
    with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors", "r") as f:
        available_guvnors = f.readline().replace("\n", "").split(" ")

    return available_guvnors


def get_core_count():
    with open("/sys/devices/system/cpu/present", "r") as f:
        "should read sth like: 0-7 for 8 cores, will not work if they are enumerated i.e. 3,5,9"
        scratch = f.readline().replace("\n", "").split("-")

    min_core = int(scratch[0])
    max_core = int(scratch[1])

    return min_core, max_core


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    if not cpufreq_set_installed():
        print("cpufreq-set utility not found, please install cpufrequtils!")
        sys.exit(1)

    if os.getuid() != 0:
        print("Please run as superuser (sudo)!")
        sys.exit(1)

    available_guvnors = get_available_governors()
    args = sys.argv

    if len(args) < 2:
        print("Please provide a valid governor one of %s" %(", ".join(available_guvnors)))
        sys.exit(1)

    "check that we have been given a valid governor"
    target_guvnor = args[1]

    if target_guvnor not in available_guvnors:
        print("%s is not a valid governor, please select one of: %s" %(target_guvnor, ", ".join(available_guvnors)))
        sys.exit(1)

    min_core, max_core = get_core_count()
    for cpu in range(min_core, max_core+1):
        print("--Setting CPU %s to %s" %(cpu, target_guvnor))
        retcode = subprocess.call(["cpufreq-set","-c","%s" %(cpu),"-g", target_guvnor])
        if retcode != 0:
            print("Encountered error")
            sys.exit(1)

    print("Success")
    sys.exit(0)

if __name__ =="__main__":
    main()