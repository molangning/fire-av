#!/usr/bin/env python3

import re
from shared_lib.lib import request_wrapper

print("[+] tor node list downloader")

content = request_wrapper("https://metrics.torproject.org/collector/recent/exit-lists/")
matches = re.findall(r"(https:\/\/collector.torproject.org\/recent\/exit-lists\/[0-9]{4}-([0-9]{2}-){4}[0-9]{2})",content)
urls = [url[0] for url in matches]
urls.sort(reverse=True)

exit_list = request_wrapper(urls[0])
exit_nodes = set()

for i in exit_list.splitlines():
    if i.startswith("ExitAddress"):
        exit_nodes.add(i.split(" ")[1]+"/32")

exit_nodes = sorted(list(dict.fromkeys(exit_nodes)))

f=open("sources/ips/tor-exit-ips-ipv4.txt","w")
f.write("\n".join(exit_nodes))