#!/usr/bin/python3

import re,os,sys,json

if len(sys.argv) < 2:
    print("[!] Not enough arguments!")
    exit(2)

targets=sys.argv[1]

regexps={}
regexps_files=[]

for root,dirs,files in os.walk('sources/regexps'):
    
    for file in files:

        if not file.endswith("ua-regex.json"):

            print("[!] File %s is not a regex file but is in the regexps directory!")
            continue

        regexps_files.append(os.path.join(root,file))

for i in regexps_files:
    
    try:
        regex=json.load(open(i))
        sep=""
        name=i

        if "/" in i:
            sep="/"

        if "\\" in i:
            sep="\\"

        if sep:
            name=i.rsplit(sep,1)[-1]

        name=name.split('-')[0]
        regexps.update({name:regex})
    
    except Exception as e:
        print("[!] Failed to load %s!"%(i))
        print("[!] Error message: %s"%(e))
        exit(2)

def check_for_regex(regexps,ua):

    # TODO Match the other flags like DOTALL and add support for multiple flags.
    for name,regexs in regexps.items():
        for regex in regexs:
            flags=re.NOFLAG
           
            if regex['flags']=="i":
                flags=re.IGNORECASE
           
            regex=regex['regex']

            if re.search(regex,ua,flags):
                return True

    return False

for i in targets.split(" "):

    contents=open(i).read().split('\n')

    for ua in contents:

        if not check_for_regex(regexps,ua):
        
            print("[!] Regex did not flag %s!" %(ua))

