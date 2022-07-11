#!/usr/bin/env python3
# pylint: disable=I0011
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0413
"""Documentation goes here ;)"""

import subprocess
from subprocess import PIPE
import os


def whoami():
    print(subprocess.call("ifconfig"))
    return

def ping2():
    print("here")
    os.system("ping -c 2 192.168.0.1 > tmp")
    print(open('tmp', 'r').read())
    os.remove('tmp')
    return

def ping(address):
    subprocess.call("ping", "-c 4 " + address)
    print("soemthing ")
    return

def run_command(cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    return subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).communicate()

def nmap_return(address):
    print("This has been passed: ", address)
    switches = "-Pn " + str(address)
    s = subprocess.call(switches, stdout=PIPE, shell=True, timeout=None) # stdin=None, stdout=None, stderr=None,
    for line in s.stdout:
        print("finally: ", line)
    output = subprocess.run('nmap -Pn 192.168.0.1', capture_output=True, text=True)
    print("Found: ", output.stdout.readline)
    return


def main_function():
    print("Staring with")
    whoami()
    ping2()
    run_command("ping -c 2 192.168.0.1")
    addresses = ["192.168.0.1/24", "192.168.1.0/24"]
    for a in addresses:
        print("A :", a)
        nmap_return(a)
        ping(a)
    print("Here in main.")
    return

# Changed: evaluate the content of variable __name__, instead of the string "__name__"
if __name__ == "__main__":
    print("Finding stuff...")
    main_function()
