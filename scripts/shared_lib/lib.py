#!/usr/bin/env python3

import time
import requests

def request_wrapper(url, headers={}, json=False):
    for i in range(1,4):

        try:
            r = requests.get(url,headers=headers)
    
            if r.status_code==200:
                print("[+] Got %s successfully!"%(url))
                break
    
            if i==3:
                print("[!] Failed to get %s."%(url))
                exit(2)
    
            print("[!] Getting %s failed(%i/3)"%(url,i))
            time.sleep(0.5)
        except Exception as e:
            print(f"[!] Got exception {e}")
    
    if json is True:
        try:
            return r.json()
        except:
            print("[+] Converting response to dictionary failed")
            exit(2)
    else:
        return r.text
