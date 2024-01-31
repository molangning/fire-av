#!/usr/bin/env python3

import re
import requests

print("[+] tor node list downloader")

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

content = request_wrapper("https://metrics.torproject.org/collector/recent/exit-lists/")
matches = re.findall(r"(https:\/\/collector.torproject.org\/recent\/exit-lists\/[0-9]{4}-([0-9]{2}-){4}[0-9]{2})",content)
urls = [url[0] for url in matches]
urls.sort(reverse=True)

exit_list = request_wrapper(urls[0])
exit_nodes = set()

for i in exit_list.splitlines():
    if i.startswith("ExitAddress"):
        exit_nodes.add(i.split(" ")[1]+"/32")

f=open("sources/ips/tor-exit-ips-ipv4.txt","w")
f.write("\n".join(exit_nodes))