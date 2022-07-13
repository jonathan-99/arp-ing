#!/usr/bin/env python3
# pylint: disable=I0011
# pylint: disable=C0103
# pylint: disable=C0325
# pylint: disable=C0413
"""Documentation goes here ;)"""

import subprocess
from subprocess import PIPE
import os
from logger import Logger
import logging

pipe = Logger(enableStdOut=True)
lanCidr = [
    "172.22.101.0/24",
    "192.168.0.0/24",
    "192.168.1.0/24"
]
lanTarget = "172.22.101.193"

# will need adjustment, or better a function that gets location on the executing OS e.g. whereis / where on script load (making it OS agnostic)
cmd_ping = "/bin/ping"
cmd_nmap = "/usr/bin/nmap"
cmd_netconfig = "/sbin/ifconfig"
os_isWin = False

def isWindows():
#def os_type():
    '''
    This function works, checking what OS you are running in order to use if or ipconfig later.
    :return: boolean - is_Windows
    '''
    try:
        if os.name == "Windows":
            #is_Windows = True
            os_isWin = True
            return True
        else:
        #     is_Windows = False
            return False
    except Exception as err:
        print("Error in tracking os type: ", err)


def whoami():
    '''
    Okay, this works and gets the return screen output. But why this and not others?
    :return:
    '''
    pipe.log("whoami: ")
    try:
        #windows_type = os_type()
        if (isWindows()):
            return subprocess.call("ifconfig")
        else:
            return subprocess.call(cmd_netconfig)
    except Exception as err:
        pipe.log("There is a problem still: {}",format(err), logLevel=logging.ERROR)


def ping2():
    '''
    This failed due to priv requirement for -c switch, so its removed.
    :return: str, however the process doesn't wait for the execution to complete.
    '''
    print("Ping2 - os.system: ")
    os.system("ping 192.168.0.1 > tmp")
    print(open('tmp', 'r').read())
    os.remove('tmp')

def ping(address: str):
    print("subprocess.call simple: ")
    subprocess.call("ping", "-c 4 " + address)
    print("something ")


def run_command(cmd: str, showOutput = True, parallel = False):
    """given shell command, returns communication tuple of stdout and stderr; or (if intended for parallel execution, returns the proc ref).
    By default will print command output after execution for syncronous command requests
    NOTE: returns the command response value, not the stdout from the command"""
    if (parallel):
        pipe.log("Parallel command invoke for {} received".format(cmd))
    else:
        pipe.log("Syncronous command invoke for {} received".format(cmd))
    
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

    if (not parallel):
        pipe.log("Command invoked. Waiting")
        proc.wait()

        pipe.log("Command waited. Polling for command response")

        if (showOutput):    
            buffer = ""
            for line in proc.stdout:
                buffer += "\n" + line.strip()
            pipe.log(buffer, logLevel=logging.DEBUG)

        result = proc.poll()

        pipe.log("Command responses: {}\n".format(str(result)))

        proc.stdout.close()
        proc.stderr.close()

        # return the result value
        return result
    else:
        # return the subproc reference for external control
        return proc


def nmap_return(address: str):
    pipe.log("Beginning nmap for {}".format(str(address)))
    command = "{} {} {}".format(cmd_nmap, "-Pn", str(address))
    
    proc = subprocess.Popen(
        command,
        # NOTE: don't specify PIPE for stdout if you want the command output to send straight to stdout
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

    nmapResponse, nmapError = proc.communicate()

    buffer = ""
    for line in nmapResponse:
        buffer += "\n{}".format(str(line).strip())

    pipe.log("Nmap results: {}\nNmap reports errors: {}".format(nmapResponse, nmapError), logLevel=logging.INFO)

def main_function():
    pipe.log("Starting with...")
    whoami()

    ## DEMO two ways of calling the run_command method, sync and async. Async called first.
    run1 = run_command("{} -c 2 {}".format(cmd_ping, "23.200.213.221"), parallel=True)
    run2 = run_command("{} -c 2 {}".format(cmd_ping, lanTarget))
    pipe.log("Response from sync call is {}".format(str(run2)))

    run1.wait()
    pipe.log("Response from initial parallel call is {}".format(str(run1.poll())))
    run1.stdout.close()
    run1.stderr.close()
    ## End of DEMO

    # port scan identified devices
    addresses = ["172.22.101.193"]
    for a in addresses:
        pipe.log("A : {}".format(a))
        nmap_return(a)
        # pinging a target that's just been scanned may not be wise
        #ping(a)
    pipe.log("Here in main")

# Changed: evaluate the content of variable __name__, instead of the string "__name__"
if __name__ == "__main__":
    pipe.log("Finding Stuff", logLevel=logging.INFO)
    main_function()
    pipe.log("Complete ARP-V Main", logLevel=logging.INFO)
