#!/usr/bin/python3

import requests,json

API_ENDPOINT="https://isc.sans.edu/api/threatcategory/research?json"
print("[+] ISC ip range downloader")
raw_ranges={}

try:
    exclude_list=json.load(open("sources/raw/exclude-list.json"))
except:
    print("[+] Converting exclude list to list failed")
    exit(2)

for i in range(1,4):
    r=requests.get(API_ENDPOINT)
    if r.status_code == 200:
        print("[+] Got a list of ip ranges!")
        
        try:
            raw_ranges=r.json()
        except:
            print("[+] Converting response to list failed")
            exit(2)
        break
    if i==3:
        print("[!] Failed to get the list of ip ranges")
        exit(2)
    print("[!] Getting json failed(%i/3)"%(i))

if not raw_ranges:
    print("[!] Retrieved list empty")
    exit(2)

print("[+] Got a list of %s ips"%(len(raw_ranges)))

ranges={}

for i in raw_ranges:
    if not i["type"]:
        continue

    if i["type"] not in list(ranges.keys()):
        ranges[i["type"]]=[[],[]]

    if "ipv4" in i.keys():
        ranges[i["type"]][0].append(i["ipv4"]+"/32")

    if "ipv6" in i.keys():
        ranges[i["type"]][1].append(i["ipv6"]+"/128")

for k,v in ranges.items():

    # anti dir traversal check
    # for untrusted lists imports

    if "/" in k:
        continue
    if "\\" in k:
        continue

    if k in exclude_list:
        continue

    result_ipv4=v[0]
    result_ipv6=v[1]
    result_ipv4=list(dict.fromkeys(result_ipv4))
    result_ipv6=list(dict.fromkeys(result_ipv6))

    print("[+] %s has %i IPv4 and %i IPv6 ranges"%(k,len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/%s-ips-ipv4.txt"%(k),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/%s-ips-ipv6.txt"%(k),'w').write(content)
