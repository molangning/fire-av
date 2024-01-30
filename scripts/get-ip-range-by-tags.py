#!/usr/bin/python3

# The flow:
# Get org to asn list from https://ftp.ripe.net/ripe/asnames/asn.txt
# then use bgp.tools asn to ip range maping

import requests,json,time,socket

print("[+] Tags to IP range downloader")

BGP_TOOLS_TAGS_API_ENDPOINT = "https://bgp.tools/tags/%s.txt"
WHOIS_IP=socket.gethostbyname("rr.level3.net")
TAGS=["vpn","tor"]

def request_wrapper(url):

    for i in range(1,4):
        r=requests.get(url, headers={"User-Agent":"Fire-AV updater"})

        if r.status_code==200:
            # print("[+] Got %s successfully!"%(url))
            break
        
        if i==3:
            print("[!] Failed to get %s."%(url))
            exit(2)
        
        print("[!] Getting %s failed(%i/3)"%(url,i))

    return r.text

def get_ranges_raw(asn):

    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((WHOIS_IP,43))
    send_string="-i origin %s\r\n"%(asn)
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

def get_ranges(asn):

    for i in range(1,4):

        try:
            data=get_ranges_raw(asn)
            break
        except Exception as e:
            print("[!] Getting %s failed(%i/3)"%(asn,i))
            print("[!] Error message: %s"%(e))

    if i==3:
        print("[!] Failed to get ASN IP ranges!")
        exit(2)

    IPv4=[]
    IPv6=[]

    for i in data.splitlines():
        if not i:
            continue

        if i.startswith("route:"):
            IPv4.append(i[6:].strip())

        if i.startswith("route6:"):
            IPv6.append(i[7:].strip())

    if not len(IPv4) and not len(IPv6):
        print("[!] No IP ranges found for %s"%(asn))

    return IPv4, IPv6

for i in TAGS:
    
    result_ipv4=set()
    result_ipv6=set()

    print("[+] Getting ASNs under %s tag"%(i))
    
    asn_list = request_wrapper(BGP_TOOLS_TAGS_API_ENDPOINT%(i)).splitlines()

    print("[+] Got a list of %i ASNs"%(len(asn_list)))
    
    for j in asn_list:
        IPv4,IPv6=get_ranges(j)
        result_ipv4.update(IPv4)
        result_ipv6.update(IPv6)
        time.sleep(0.5)

    result_ipv4=list(result_ipv4)
    result_ipv6=list(result_ipv6)

    print("[+] Got a list of %i IPv4 and %i IPv6 ranges"%(len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/by-tags/%s-ips-ipv4.txt"%(i),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/by-tags/%s-ips-ipv6.txt"%(i),'w').write(content)