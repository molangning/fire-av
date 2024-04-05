#!/usr/bin/python3

import requests,json

API_ENDPOINT="https://api.github.com/meta"
print("[+] Github ip range downloader")
raw_ranges={}

def request_wrapper(url):

    for i in range(1,4):
        r=requests.get(url)
        if r.status_code==200:
            # print("[+] Got %s successfully!"%(url))
            break
        if i==3:
            print("[!] Failed to get %s."%(url))
            exit(2)
        print("[!] Getting %s failed(%i/3)"%(url,i))

    return r.text

raw_ranges = json.loads(request_wrapper(API_ENDPOINT))
print("[+] Got a list of ip ranges!")

if not raw_ranges:
    print("[!] Retrieved list empty")
    exit(2)

keys = []
ranges = {}

for k in raw_ranges.keys():

    if not isinstance(raw_ranges[k], list):
        print(f"[!] Skipping {k} as it is not a list")
        continue

    if not raw_ranges[k][0].replace(".", "").replace("/", "").isnumeric():
        print(f"[!] Skipping {k} as it is not an ip range")
        continue

    keys.append(k)

for k in keys:

    new_name = k.replace("_", "-")

    if not k.startswith("github"):
        new_name = f"github-{k}"

    ranges[new_name] = [[],[]]

    for ip_range in raw_ranges[k]:

        if ":" in ip_range:
            ranges[new_name][1].append(ip_range)

        elif "." in ip_range:
            ranges[new_name][0].append(ip_range)

for k,v in ranges.items():

    # anti dir traversal check
    # for untrusted lists imports

    if "/" in k:
        continue
    if "\\" in k:
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
