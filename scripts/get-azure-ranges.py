#!/usr/bin/python3

import re
from shared_lib.lib import request_wrapper

MICROSOFT_ENPOINT = "https://www.microsoft.com/en-us/download/details.aspx?id=56519"
USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.3"

print("[+] Azure ip range downloader")

contents=request_wrapper(MICROSOFT_ENPOINT, headers={"User-Agent":USERAGENT})

download_url=re.findall(r"https:\/\/download.microsoft.com\/download\/.*?\.json",contents)[0]

azure_ips=request_wrapper(download_url, json=True)['values']

azure_ipv4=[]
azure_ipv6=[]

for i in azure_ips:
    for j in i["properties"]["addressPrefixes"]:
        if "." in j:
            azure_ipv4.append(j)
        if ":" in j:
            azure_ipv6.append(j)

azure_ipv4=sorted(list(dict.fromkeys(azure_ipv4)))
azure_ipv6=sorted(list(dict.fromkeys(azure_ipv6)))

if len(azure_ipv4) > 0:
    content="\n".join(azure_ipv4)
    open("sources/ips/azure-ips-ipv4.txt",'w').write(content)

if len(azure_ipv6) > 0:
    content="\n".join(azure_ipv6)
    open("sources/ips/azure-ips-ipv6.txt",'w').write(content)
