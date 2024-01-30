#!/usr/bin/env python3

import re,os

print("[+] IPv4 regex check")

files = []
dirs = ['sources/','blacklists/','whitelists/']
IPV4_REGEX=r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}\/(3[0-2]|[1-2][0-9]|[1-3])$"

for i in dirs:
    for root,_,file_list in os.walk(i):
        for file in file_list:
            if 'ipv4' not in file:
                continue
            files.append(os.path.join(root,file))

passed_check=True

for i in files:
    f=open(i)
    contents=f.read()

    if len(contents) == 0:
        continue # Empty file

    for j in contents.split('\n'):
        if not re.match(IPV4_REGEX,j):
            print("[!] %s did not pass the IPv4 regex check"%(j))
            print("[!] Offending file: %s"%(i))
            passed_check=False
    # print("[+] %s passed IPv4 regex check"%(i))

if not passed_check:
    print("[!] One or multiple checks failed for ipv4 ranges")
    exit(2)

print("[+] All IPv4 checks succeeded")
exit(0)
