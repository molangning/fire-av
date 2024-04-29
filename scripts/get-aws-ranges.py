#!/usr/bin/python3

from shared_lib.lib import request_wrapper

AWS_ENDPOINT = "https://ip-ranges.amazonaws.com/ip-ranges.json"

print("[+] AWS ip range downloader")

ranges=request_wrapper(AWS_ENDPOINT, json=True)
print("[+] Got a list of ip ranges!")

if not ranges:
    print("[!] Retrieved dictionary empty")
    exit(2)

if not ranges["prefixes"]:
    print("[!] Retrieved dictionary key prefixes missing")
    exit(2)

ipv4_ranges=[]
ipv6_ranges=[]

for i in ranges["prefixes"]:
    ipv4_ranges.append(i["ip_prefix"])

for i in ranges["ipv6_prefixes"]:
    ipv6_ranges.append(i["ipv6_prefix"])

ipv4_ranges=sorted(list(dict.fromkeys(ipv4_ranges)))
ipv6_ranges=sorted(list(dict.fromkeys(ipv6_ranges)))

f=open("sources/ips/aws-ips-ipv4.txt","w").write('\n'.join(ipv4_ranges))
f=open("sources/ips/aws-ips-ipv6.txt","w").write('\n'.join(ipv6_ranges))