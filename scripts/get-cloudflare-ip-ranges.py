#!/usr/bin/python3

from shared_lib.lib import request_wrapper

CLOUDFLARE_API_ENDPOINT="https://api.cloudflare.com/client/v4/ips?networks=jdcloud"

print("[+] Cloudflare ip range getter")

cloudflare_ranges = request_wrapper(CLOUDFLARE_API_ENDPOINT, json=True)["result"]

if not cloudflare_ranges:
    print("[!] Cloudflare ranges empty!")
    exit(2)
    
if not "jdcloud_cidrs" in cloudflare_ranges.keys():
    print("[!] Cloudflare jd ranges empty!")
    exit(2)

if not "ipv4_cidrs" in cloudflare_ranges.keys():
    print("[!] Cloudflare IPv4 ranges empty!")
    exit(2)

if not "ipv6_cidrs" in cloudflare_ranges.keys():
    print("[!] Cloudflare IPv6 ranges empty!")
    exit(2)

cloudflare_jd_ipv4_ranges = []
cloudflare_jd_ipv6_ranges = []

for jd_cloud_range in cloudflare_ranges["jdcloud_cidrs"]:

    if ":" in jd_cloud_range:
        cloudflare_jd_ipv6_ranges.append(jd_cloud_range)

    elif "." in jd_cloud_range:
        cloudflare_jd_ipv4_ranges.append(jd_cloud_range)


cloudflare_ipv4_ranges = cloudflare_ranges["ipv4_cidrs"]
cloudflare_ipv6_ranges = cloudflare_ranges["ipv6_cidrs"]

cloudflare_ipv4_ranges = sorted(list(dict.fromkeys(cloudflare_ipv4_ranges)))
cloudflare_ipv6_ranges = sorted(list(dict.fromkeys(cloudflare_ipv6_ranges)))

cloudflare_jd_ipv4_ranges = sorted(list(dict.fromkeys(cloudflare_ipv4_ranges)))
cloudflare_jd_ipv6_ranges = sorted(list(dict.fromkeys(cloudflare_ipv6_ranges)))

f=open("sources/ips/cloudflare-jd-cloud-ips-ipv4.txt","w").write('\n'.join(cloudflare_jd_ipv4_ranges))
f=open("sources/ips/cloudflare-jd-cloud-ips-ipv6.txt","w").write('\n'.join(cloudflare_jd_ipv6_ranges))

f=open("sources/ips/cloudflare-cdn-only-ips-ipv4.txt","w").write('\n'.join(cloudflare_ipv4_ranges))
f=open("sources/ips/cloudflare-cdn-only-ips-ipv6.txt","w").write('\n'.join(cloudflare_ipv6_ranges))

print("[+] Got all IP address ranges")