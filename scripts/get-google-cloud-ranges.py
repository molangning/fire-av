#!/usr/bin/python3

from shared_lib.lib import request_wrapper

GOOGLE_ENDPOINT="https://www.gstatic.com/ipranges/cloud.json"

print("[+] Google cloud ip range downloader")
ranges=request_wrapper(GOOGLE_ENDPOINT, json=True)

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

ipv4_ranges=sorted(list(dict.fromkeys(ipv4_ranges)))
ipv6_ranges=sorted(list(dict.fromkeys(ipv6_ranges)))

f=open("sources/ips/google-cloud-ips-ipv4.txt","w").write('\n'.join(ipv4_ranges))
f=open("sources/ips/google-cloud-ips-ipv6.txt","w").write('\n'.join(ipv6_ranges))