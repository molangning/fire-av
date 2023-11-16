#!/usr/bin/env python3

import re,os

dirs = ['sources/','blacklists/','whitelists/']
files = []
IPV4_REGEX=r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}\/(3[0-2]|[1-2][0-9]|[1-3])$"

for i in dirs:
    for j in os.listdir(i):
        if 'ips' not in j:
            continue
        files.append(os.path.join(i,j))

for i in files:
    f=open(i)
    contents=f.read()

    if len(contents) == 0:
        continue # Empty file

    for j in contents.split('\n'):
        if not re.match(IPV4_REGEX,j):
            print("[!] %s did not pass the regex check"%(j))
            exit(2)
    print("[+] %s passed the check"%(i))

print("IPv4 checks succeeded")
exit(0)
