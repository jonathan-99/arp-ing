## Arping

Nice to fire off a quick arp (using nmap) to see what's on your network.

# isWindows
Uses standard indicators to assess whether current OS is Win - used by `whoami`

# whoami
Executes an `ip addr show` equiv, `ifconfig` if Win, `ipconfig` if Nix

# ping2
Sandbox method (untouched in this commit)

# ping
Sandbox method (untouched in this commit)

# run_command
Generic shell executor, optional params for
- Showing the command output in stdout (default)
- Executing the command in parallel (default is syncronous)

# nmap_return
Executes nmap for a given IP, with `-Pn` param
