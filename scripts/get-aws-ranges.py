#!/usr/bin/python3

# TODO IPv6 ranges

import requests

print("[+] AWS ip range downloader")
ranges={}

for i in range(1,4):
    r=requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
    if r.status_code == 200:
        print("[+] Got a list of ip ranges!")
        
        try:
            ranges=r.json()
        except:
            print("[+] Converting response to dictionary failed")
            exit(2)

        break
    if i==3:
        print("[!] Failed to get the list of ip ranges")
        exit(2)
    print("[!] Getting json failed(%i/3)")

if not ranges:
    print("[!] Retrieved dictionary empty")
    exit(2)

if not ranges["prefixes"]:
    print("[!] Retrieved dictionary key prefixes missing")
    exit(2)

ipv4_ranges=[]

for i in ranges["prefixes"]:
    ipv4_ranges.append(i["ip_prefix"])

f=open("sources/ips/aws-ips-ipv4.txt","w").write('\n'.join(ipv4_ranges))

ipv6_ranges=[]

for i in ranges["ipv6_prefixes"]:
    ipv6_ranges.append(i["ipv6_prefix"])

f=open("sources/ips/aws-ips-ipv6.txt","w").write('\n'.join(ipv6_ranges))