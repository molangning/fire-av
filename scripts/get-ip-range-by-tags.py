#!/usr/bin/python3

# The flow:
# Get org to asn list from https://ftp.ripe.net/ripe/asnames/asn.txt
# then use bgp.tools asn to ip range maping

import json
from shared_lib.lib import request_wrapper

print("[+] Tags to IP range downloader")

BGP_TOOLS_TAGS_API_ENDPOINT = "https://bgp.tools/tags/%s.txt"
TAGS=["vpn","tor"]
ASN_IPV4_LIST=json.load(open("sources/raw/asn_ipv4.json"))
ASN_IPV6_LIST=json.load(open("sources/raw/asn_ipv6.json"))

def get_ranges(asn):

    if not asn.startswith("AS"):
        asn = "AS" + asn

    IPv4=[]
    IPv6=[]

    if asn in ASN_IPV4_LIST:
        IPv4=ASN_IPV4_LIST[asn]

    if asn in ASN_IPV6_LIST:
        IPv6=ASN_IPV6_LIST[asn]    

    if not IPv4 and not IPv6:
        print("[!] No IP ranges found for %s"%(asn))

    return IPv4,IPv6

for i in TAGS:
    
    result_ipv4=set()
    result_ipv6=set()

    print("[+] Getting ASNs under %s tag"%(i))
    
    asn_list = request_wrapper(BGP_TOOLS_TAGS_API_ENDPOINT%(i), headers={"User-Agent":"Fire-AV updater"}).splitlines()

    print("[+] Got a list of %i ASNs"%(len(asn_list)))
    
    for j in asn_list:

        IPv4,IPv6=get_ranges(j)
        result_ipv4.update(IPv4)
        result_ipv6.update(IPv6)

    result_ipv4=sorted(list(dict.fromkeys(result_ipv4)))
    result_ipv6=sorted(list(dict.fromkeys(result_ipv6)))

    print("[+] Got a list of %i IPv4 and %i IPv6 ranges"%(len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/by-tags/%s-ips-ipv4.txt"%(i),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/by-tags/%s-ips-ipv6.txt"%(i),'w').write(content)