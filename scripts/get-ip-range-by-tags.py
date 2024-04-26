#!/usr/bin/python3

# The flow:
# Get org to asn list from https://ftp.ripe.net/ripe/asnames/asn.txt
# then use bgp.tools asn to ip range maping

import requests,json,time,socket,random

print("[+] Tags to IP range downloader")

BGP_TOOLS_TAGS_API_ENDPOINT = "https://bgp.tools/tags/%s.txt"
WHOIS_IPS=["rr.Level3.net", "rr.ntt.net", "whois.radb.net", "irr.bgp.net.br"]
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

    for i in random.sample(WHOIS_IPS, len(WHOIS_IPS)):
        
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect((socket.gethostbyname(i), 43))
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
        print("[!] No IP ranges found for %s"%(asn))

    return IPv4,IPv6

for i in TAGS:
    
    result_ipv4=set()
    result_ipv6=set()

    print("[+] Getting ASNs under %s tag"%(i))
    
    asn_list = request_wrapper(BGP_TOOLS_TAGS_API_ENDPOINT%(i)).splitlines()

    print("[+] Got a list of %i ASNs"%(len(asn_list)))

    # Tells the user every 10 asn about the status

    counter=0
    current=1
    limit=10
    
    for j in asn_list:

        counter+=1

        IPv4,IPv6=get_ranges(j)
        result_ipv4.update(IPv4)
        result_ipv6.update(IPv6)
        time.sleep(0.5)

        if counter == limit:
            counter=0
            print("[+] %i ASNs left to check"%(len(asn_list)-current))
        
        current+=1

    result_ipv4=sorted(list(dict.fromkeys(result_ipv4)))
    result_ipv6=sorted(list(dict.fromkeys(result_ipv6)))

    print("[+] Got a list of %i IPv4 and %i IPv6 ranges"%(len(result_ipv4),len(result_ipv6)))

    if len(result_ipv4) > 0:
        content="\n".join(result_ipv4)
        open("sources/ips/by-tags/%s-ips-ipv4.txt"%(i),'w').write(content)

    if len(result_ipv6) > 0:
        content="\n".join(result_ipv6)
        open("sources/ips/by-tags/%s-ips-ipv6.txt"%(i),'w').write(content)