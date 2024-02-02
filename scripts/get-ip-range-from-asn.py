#!/usr/bin/python3

# The flow:
# Get org to asn list from https://ftp.ripe.net/ripe/asnames/asn.txt
# then use bgp.tools asn to ip range maping

import requests
import json
import time
import socket
import random

print("[+] Name to IP range downloader")

RAW_ASN_LIST="https://ftp.ripe.net/ripe/asnames/asn.txt"
ASN_SEARCH=json.load(open("sources/raw/asn-list.json"))
WHOIS_IPS=["whois.in.bell.ca", "irr.bboi.net", "rr.Level3.net", "rr.ntt.net", "whois.radb.net", "irr.bgp.net.br"]

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

def get_ranges_raw(asn):

    for i in random.sample(WHOIS_IPS, len(WHOIS_IPS)):
        
        try:

            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect((socket.gethostbyname(i), 43))
            send_string="-i origin AS%s\r\n"%(asn)
            s.sendall(send_string.encode("utf-8"))
            chunk=""
            data=""

            while True:
                chunk=s.recv(4096)
                if not chunk:
                    break
                chunk=chunk.decode('utf-8')
                data+=chunk
                if chunk.endswith("\n\n\n"):
                    break

            return data

        except Exception as e:
            print("[!] Failed to get %s from %s"%(asn,i))
            print("[!] Error message: %s"%(e))

    return None

def get_ranges(asn):

    data=get_ranges_raw(asn)

    if not data:
        print("[!] Unable to get ip ranges from any routing registries!")

    IPv4=[]
    IPv6=[]

    for i in data.split('\n'):
        if not i:
            continue

        if i.startswith("route:"):
            IPv4.append(i[6:].strip())

        if i.startswith("route6:"):
            IPv6.append(i[7:].strip())

    if not len(IPv4) and not len(IPv6):
        print("[!] No IP ranges found for AS%s"%(asn))

    return IPv4,IPv6

asn_lists_raw=request_wrapper(RAW_ASN_LIST)
print("[+] Got raw ASNs list")
asn_list=[]

for i in asn_lists_raw.split('\n'):
    
    if not i:
        continue

    asn, name_and_cc=i.split(" ",1)

    if "reserved by" in name_and_cc:
        name=name_and_cc
        cc="zz"
    else:
        name,cc=name_and_cc.rsplit(", ",1)

    asn_list.append([asn,name,cc])

print("[+] loaded a list of %s ASNs"%(len(asn_list)))

target_asn=[]

def matcher(match_cond,content):

    content=content.lower()
    matches=match_cond["match"]
    rejects=match_cond["reject"]

    for i in rejects:
        if i.lower() in content:
            return False

    for i in matches:
        if i.lower() in content:
            return True

    return False

for file_name,search_cond in ASN_SEARCH.items():
    result=[]
    
    for i in asn_list:
        if matcher(search_cond,i[1]):
            result.append(i[0])

    target_asn.append([file_name,result])

for i in target_asn:
    name,asn_list=i
    # anti dir traversal check
    # for untrusted lists imports

    if "/" in name:
        continue
    if "\\" in name:
        continue

    asn_list=list(set(asn_list))
    asn_list=random.sample(asn_list, len(asn_list))

    result_ipv4=[]
    result_ipv6=[]

    print("[+] Getting %s ASNs"%(name))
    print("[+] %s's ASNs: %s"%(name,",".join(asn_list)))
    
    for j in asn_list:

        IPv4,IPv6=get_ranges(j)
        result_ipv4+=IPv4
        result_ipv6+=IPv6
        time.sleep(0.5)

    result_ipv4=list(dict.fromkeys(result_ipv4))
    result_ipv6=list(dict.fromkeys(result_ipv6))

    print("[+] Got a list of %i IPv4 and %i IPv6 ranges"%(len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/%s-ips-ipv4.txt"%(name),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/%s-ips-ipv6.txt"%(name),'w').write(content)