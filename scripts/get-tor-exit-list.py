#!/usr/bin/env python3
import requests

print("[+] tor node list downloader")

for i in range(1,4):
    r=requests.get("https://check.torproject.org/torbulkexitlist")
    if r.status_code == 200:
        print("[+] Got a list of tor nodes!")
        break
    if i==3:
        print("[!] Failed to get list of tor exits.")
        exit(2)
    print("[!] Getting tor exits failed(%i/3)")

contents=[]

for i in r.text.split('\n'):
    if len(i)==0:
        continue

    contents.append(i+"/32")

f=open("sources/ips/tor-exit-ips-ipv4.txt","w")
f.write("\n".join(contents))