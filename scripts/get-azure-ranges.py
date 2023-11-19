#!/usr/bin/python3

import requests,json,re

print("[+] Azure ip range downloader")

def request_wrapper(url, headers={}):

    for i in range(1,4):
        r=requests.get(url,headers=headers)
        if r.status_code==200:
            print("[+] Got %s successfully!"%(url))
            break
        if i==3:
            print("[!] Failed to get %s."%(url))
            exit(2)
        print("[!] Getting %s failed(%i/3)"%(url,i))

    return r.text

ua_dict=json.loads(request_wrapper("https://www.useragents.me/api"))

best_ua = ua_dict["data"][0]['ua']

contents=request_wrapper("https://www.microsoft.com/en-us/download/details.aspx?id=56519",headers={"User-Agent":best_ua})

open("temp.txt","w").write(contents)

download_url=re.findall(r"https:\/\/download.microsoft.com\/download\/.*?\.json",contents)[0]

azure_ips=json.loads(request_wrapper(download_url))['values']

azure_ipv4=[]
azure_ipv6=[]

for i in azure_ips:
    for j in i["properties"]["addressPrefixes"]:
        if "." in j:
            azure_ipv4.append(j)
        if ":" in j:
            azure_ipv6.append(j)

azure_ipv4=list(dict.fromkeys(azure_ipv4))
azure_ipv6=list(dict.fromkeys(azure_ipv6))

if len(azure_ipv4) > 0:
    content="\n".join(azure_ipv4)
    open("sources/ips/azure-ips-ipv4.txt",'w').write(content)

if len(azure_ipv6) > 0:
    content="\n".join(azure_ipv6)
    open("sources/ips/azure-ips-ipv6.txt",'w').write(content)
