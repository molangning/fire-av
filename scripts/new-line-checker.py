#!/usr/bin/env python3

import os

print("[+] New line check")

files = []
dirs = ['sources/','blacklists/','whitelists/']
ignore_file_exts = ["json", "gz", "zip", "mmdb", "csv"]

for i in dirs:
    for root,_,file_list in os.walk(i):
        for file in file_list:
            for ignore_ext in ignore_file_exts:
                files.append(os.path.join(root,file))

passed_check=True

for i in files:
    
    if i.rsplit(".",1)[-1] in ignore_file_exts:
        continue
    
    print(i)

    contents = open(i,"r").read()

    if len(contents) == 0:
        continue
    
    if contents[-1] == '\n':
        print("[!] %s ends with a new line"%(i))
        passed_check=False

if not passed_check:
    print("[!] One or multiple checks failed for new lines")
    exit(2)

print("[+] All files passed checks")
exit(0)
