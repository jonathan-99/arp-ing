import subprocess

def nmap_return(address):
    print("This has been passed: ", address)
    switches = "-Pn " + str(address)
#    subprocess.call(switches, stdin=None, stout=None, sterr=None, shell=False, timeout=None)
    output = subprocess.getoutput('nmap -Pn 192.168.0.1')
    print("Found: ",output)
    return

def main_function():
    print("Staring with")
    addresses = ["192.168.0.1/24","192.168.1.0/24"]
    for a in addresses:
        print("A :", a)
        nmap_return(a)
    print("Here in main.")
    return


if "__name__" == "__main__":
    print("Finding stuff...")
    main_function()
