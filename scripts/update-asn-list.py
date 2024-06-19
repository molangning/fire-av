#!/usr/bin/env python3

import json
import os

from shared_lib.lib import request_wrapper

BASE_PATH = "sources/raw/"

HISTORY_FILE = "history.json"
IPV4_FILE = "asn_ipv4.json"
IPV6_FILE = "asn_ipv6.json"

RESOLVED_HISTORY_FILE = os.path.join(BASE_PATH, HISTORY_FILE)
RESOLVED_IPV4_FILE = os.path.join(BASE_PATH, IPV4_FILE)
RESOLVED_IPV6_FILE = os.path.join(BASE_PATH, IPV6_FILE)

ASN_IPV4_LIST = "https://github.com/molangning/irr-tracker/raw/main/sources/asn_ipv4.json"
ASN_IPV6_LIST = "https://github.com/molangning/irr-tracker/raw/main/sources/asn_ipv6.json"
ASN_LIST_ENDPOINT = "https://api.github.com/repos/molangning/irr-tracker/git/trees/main:sources%2F"

remote_file_hash = ""
history = {}

if os.path.isfile(RESOLVED_HISTORY_FILE):
    history = json.load(open(RESOLVED_HISTORY_FILE))     
else:
    print("[!] History file not found.")

print("[+] Getting asn list hashes")
sources_hashes = request_wrapper(ASN_LIST_ENDPOINT, json=True)
print("[+] Got asn list hashes")

remote_file_hash = ""
got_ipv4 = False
got_ipv6 = False
to_check = ""

for file in sources_hashes["tree"]:
    if file["path"] == IPV4_FILE:
        to_check = RESOLVED_IPV4_FILE
        source_url = ASN_IPV4_LIST
        remote_file_hash = file["sha"]

    elif file["path"] == IPV6_FILE:
        to_check = RESOLVED_IPV6_FILE
        source_url = ASN_IPV6_LIST
        remote_file_hash = file["sha"]

    else:
        continue

    if to_check in history.keys() and history[to_check] == remote_file_hash:
        print(f"[+] File {to_check} is still the same.")
        continue

    print(f"[+] Updating {to_check}")
    open(to_check, "w").write(request_wrapper(source_url))

    print("[+] Updated file")
    history[to_check] = remote_file_hash
    json.dump(history, open(RESOLVED_HISTORY_FILE, "w"), indent=4)
