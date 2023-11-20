#!/usr/bin/python3

import requests

print("[+] Google cloud ip range downloader")
ranges={}

for i in range(1,4):
    r=requests.get("https://www.gstatic.com/ipranges/cloud.json")
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
    print("[!] Getting json failed(%i/3)"%(i))

if not ranges:
    print("[!] Retrieved dictionary empty")
    exit(2)

if not ranges["prefixes"]:
    print("[!] Retrieved dictionary key prefixes missing")
    exit(2)

ipv4_ranges=[]
ipv6_ranges=[]

for i in ranges["prefixes"]:

    dict_keys=i.keys()
    if "ipv4Prefix" in dict_keys:
        ipv4_ranges.append(i['ipv4Prefix'])

    if "ipv6Prefix" in dict_keys:
        ipv6_ranges.append(i['ipv6Prefix'])

f=open("sources/ips/google-cloud-ips-ipv4.txt","w").write('\n'.join(ipv4_ranges))
f=open("sources/ips/google-cloud-ips-ipv6.txt","w").write('\n'.join(ipv6_ranges))