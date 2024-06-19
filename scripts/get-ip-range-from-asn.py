#!/usr/bin/python3

import json
import random
from shared_lib.lib import request_wrapper

print("[+] Name to IP range downloader")

RAW_ASN_LIST="https://ftp.ripe.net/ripe/asnames/asn.txt"
ASN_SEARCH=json.load(open("sources/raw/asn-list.json"))
ASN_IPV4_LIST=json.load(open("sources/raw/asn_ipv4.json"))
ASN_IPV6_LIST=json.load(open("sources/raw/asn_ipv6.json"))

def get_ranges(asn):

    IPv4=[]
    IPv6=[]

    asn = "AS" + asn

    if asn in ASN_IPV4_LIST:
        IPv4=ASN_IPV4_LIST[asn]

    if asn in ASN_IPV6_LIST:
        IPv6=ASN_IPV6_LIST[asn]

    if not IPv4 and not IPv6:
        print("[!] No IP ranges found for %s"%(asn))

    return IPv4, IPv6

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

    result_ipv4=sorted(list(dict.fromkeys(result_ipv4)))
    result_ipv6=sorted(list(dict.fromkeys(result_ipv6)))

    print("[+] Got a list of %i IPv4 and %i IPv6 ranges"%(len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/%s-ips-ipv4.txt"%(name),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/%s-ips-ipv6.txt"%(name),'w').write(content)
