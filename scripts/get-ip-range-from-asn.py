#!/usr/bin/python3

# The flow:
# Get org to asn list from https://ftp.ripe.net/ripe/asnames/asn.txt
# then query shadow server api

import requests,json,time

print("[+] Name to IP range downloader")

RAW_ASN_LIST="https://ftp.ripe.net/ripe/asnames/asn.txt"
API_ASN_LOOKUP_v4="https://api.shadowserver.org/net/asn?prefix=%s"
API_ASN_LOOKUP_v6="https://api.shadowserver.org/net/asn?prefix=%s&v6"
ASN_SEARCH=json.load(open("sources/raw/asn-list.json"))

def request_wrapper(url):

    for i in range(1,4):
        r=requests.get(url)
        if r.status_code==200:
            print("[+] Got %s successfully!"%(url))
            break
        if i==3:
            print("[!] Failed to get %s."%(url))
            exit(2)
        print("[!] Getting %s failed(%i/3)"%(url,i))

    return r.text


asn_lists_raw=request_wrapper(RAW_ASN_LIST)
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

for file_name,search_terms in ASN_SEARCH.items():
    result=[]
    
    for i in asn_list:
        for j in search_terms:
            if j.lower() in i[1].lower():
                result.append(i[0])

    target_asn.append([file_name,result])

for i in target_asn:
    name,asn_list=i
    result_ipv4=[]
    result_ipv6=[]

    print("[+] Getting %s ASNs"%(name))

    for j in asn_list:
        result_ipv4+=json.loads(request_wrapper(API_ASN_LOOKUP_v4%(j)))
        time.sleep(0.5)
        # Backend throwing weird results for ipv6 queries
        # Should be fixed within next week
        # TODO check if it gets fixed
        #
        # result_ipv6+=json.loads(request_wrapper(API_ASN_LOOKUP_v6%(j)))
        # time.sleep(0.5)

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/%s-ips-ipv4.txt"%(name),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/%s-ips-ipv6.txt"%(name),'w').write(content)