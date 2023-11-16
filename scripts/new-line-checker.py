#!/usr/bin/env python3

import os

print("[+] New line check")

files = []
dirs = ['sources/','blacklists/','whitelists/']

for i in dirs:
    for j in os.listdir(i):
        files.append(os.path.join(i,j))

for i in files:
    f=open(i)
    contents=f.read()
    if contents[:-1] == '\n':
        print("[!] %s ends with a new line"%s(i))
        exit(2)
    # print("[+] %s passed new line check"%(i))

print("[+] All files passed checks")
exit(0)