#!/usr/bin/python3

import re,os,json

print("[+] JSON file syntax check")

dirs=["sources/regexps"]
regexps_files=[]

for i in dirs:
    for root,_,file_list in os.walk(i):
        for file in file_list:
            if '.json' not in file:
                continue
            regexps_files.append(os.path.join(root,file))

for i in regexps_files:

    try:
        regex_json=json.load(open(i))
    except Exception as e:
        print("[!] Error in decoding file %s!"%(i))
        print("[!] Exception: %s"%(e.msg))
        exit(2)

    for j in regex_json:
        if ['regex', 'flags']!=list(j.keys()):
            print("[!] %s does not fit the regex format!"%(i))
            exit(2)

print("[+] Regexps checks passed")

try:
    asn_list=json.load(open("sources/raw/asn-list.json"))
except Exception as e:
    print("[!] Error in decoding asn list!")
    print("[!] Exception: %s"%(e.msg))
    exit(2)

for k,v in asn_list.items():

    if ['match', 'reject']!=list(v.keys()):
        print("[!] %s does not fit the asn format!"%(i))
        exit(2)

    if not isinstance(v["match"],list):
        print("[!] The value of match is not a list!")
        print("[!] Key name: %s"%(k))
        exit(2)

    if not isinstance(v["reject"],list):
        print("[!] The value of reject is not a list!")
        print("[!] Key name: %s"%(k))
        exit(2)

print("[+] ASN list checks passed")

for i in regexps_files:
    try:
        raw_content=json.load(open(i))
        json.dump(raw_content,open(i,"w"),indent=4)
    except Exception as e:
        print("[!] Error in formating file %s!"%(i))
        print("[!] Exception: %s"%(e.msg))
        exit(2)

try:
    json.dump(asn_list,open("sources/raw/asn-list.json","w"),indent=4)
except Exception as e:
    print("[!] Error in formating file %s!"%(i))
    print("[!] Exception: %s"%(e.msg))
    exit(2)