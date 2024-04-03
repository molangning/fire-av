#!/usr/bin/python3

import requests,re,time

DIR_LIST="https://lists.blocklist.de/lists/"

print("[+] Blocklist.de ip range downloader")
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

root_dir_list = request_wrapper(DIR_LIST)
files = re.findall(r"([0-9a-z]+\.txt)\">", root_dir_list)

for source_list in files:
    raw_ranges[source_list[:-4]] = request_wrapper(DIR_LIST+source_list).splitlines()
    print(f"[+] Got {source_list}")
    time.sleep(0.5)

if not raw_ranges:
    print("[!] Retrieved list empty")
    exit(2)

print("[+] Got a list of %s ips tags"%(len(raw_ranges)))

ranges={}

for tag, ips in raw_ranges.items():

    if tag not in list(ranges.keys()):
        ranges[tag]=[[],[]]

    for ip in ips:
        if "." in ip:
            ranges[tag][0].append(ip+"/32")

        elif ":" in ip:
            ranges[tag][1].append(ip+"/128")

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
        open("sources/ips/blocklist-de/%s-ips-ipv4.txt"%(k),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/blocklist-de/%s-ips-ipv6.txt"%(k),'w').write(content)
