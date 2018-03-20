#!/usr/bin/python
#this works with python2 and 3

import sys
import os
import subprocess
import signal

"""
set the core frequency of all cores to the given value in GHz
"""

def cpufreq_set_installed():
    p = subprocess.Popen(["/usr/bin/which","cpufreq-set"], stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return False
    else:
        return True

def get_core_count():
    with open("/sys/devices/system/cpu/present", "r") as f:
        "should read sth like: 0-7 for 8 cores, will not work if they are enumerated i.e. 3,5,9"
        scratch = f.readline().replace("\n", "").split("-")

    min_core = int(scratch[0])
    max_core = int(scratch[1])

    return min_core, max_core

def check_freq_limits(min_core):
    #this assumes that all cores have the same limitations
    with open("/sys/devices/system/cpu/cpu%s/cpufreq/cpuinfo_min_freq" %min_core, "r") as f:
        min_freq = float(f.readline().replace("\n", ""))

    with open("/sys/devices/system/cpu/cpu%s/cpufreq/cpuinfo_max_freq" %min_core, "r") as f:
        max_freq = float(f.readline().replace("\n", ""))

    return min_freq, max_freq


def sigint_handler(signal, stackframe):
    print("Exiting on user interrupt")
    sys.exit(130)

def main():

    signal.signal(signal.SIGINT, sigint_handler)

    if not cpufreq_set_installed():
        print("cpufreq-set utility not found, please install cpufrequtils!")
        sys.exit(1)

    if os.getuid() != 0:
        print("Please run as superuser (sudo)!")
        sys.exit(1)


    min_core, max_core = get_core_count()

    min_freq, max_freq = check_freq_limits(min_core)

    min_freq = min_freq/1000000
    max_freq = max_freq/1000000

    args = sys.argv
    if len(args) < 2:
        print("Please provide a valid frequency within %sGHz - %sGHz " %(min_freq, max_freq))
        sys.exit(1)

    target_freq = float(args[1].replace("GHz",""))

    if target_freq < min_freq or target_freq > max_freq:
        print("Please provide a valid frequency %sGHz - %sGHz for cores %s through %s" %(min_freq, max_freq, min_core, max_core))
        sys.exit(1)

    for cpu in range(min_core,max_core+1):
        print("--Setting CPU %s max frequency to %s" %(cpu, target_freq))
        retcode = subprocess.call(["cpufreq-set", "-c", str(cpu),"-u", "%sGHz" %target_freq])
        if retcode != 0:
            print("cpufreq-set encountered an error with core %s" %(cpu))
            sys.exit(1)
    
    print("Success")
    sys.exit(0)

if __name__ == "__main__":
    main()