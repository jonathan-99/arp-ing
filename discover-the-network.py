import argparse
import arp_v


"""This is the main function which holds all arguments to effectively control arp-v.
"""
def main_function() -> int:
    parser = argparse.ArgumentParser()

    # this chooses to use a ping command
    parser.add_argument("-p", "--ping", help="2 ICMPs sent to D class by default")

    # this chooses a specific ip address, default 127.0.0.1
    parser.add_argument("-ip", "--ipaddr", type=str,
                        default="127.0.0.1",
                        help="enter a specific ip address - 192.168.0.1")

    # this chooses a subnet mask, default /24
    parser.add_argument("-m", "--mask", type=str,
                        default="/24",
                        choices=['/8', '/16', '/24'],
                        help="options of /8, /16, or /24")

    args = parser.parse_args()

    if args.ping:
        if arp_v.check_os() == True:
            output = arp_v.run_command("ping -c 2")
            if output != "":
                print("Done that command {}".format(output))
                return 0
        else:
            print("This needs linux to function")
    elif args.ping != "":
        input = str("nmap -Pn " + args.ipaddr + args.mask)
        output = arp_v.run_command(input)
        print("This bit did: ", output)
    else:
        pass
    return 0

if __name__ == "__main__":
    main_function()