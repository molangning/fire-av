#!/usr/bin/env python3

import requests
import socket

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
    
def get_ranges_raw(asn, whois_ips, full_run=False):

    result = {}

    for i in whois_ips:
        
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect((socket.gethostbyname(i), 43))
            send_string="-i origin AS%s\r\n"%(asn)
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

            if "route:" not in data and "route6:" not in data and full_run is False:
                print("%s returned no ipv4 or ipv6 ranges for AS%s"%(i, asn))
                continue
            
            if full_run is False:
                return data

            result[i] = data

        except Exception as e:
            print("[!] Failed to get %s from %s"%(asn,i))
            print("[!] Error message: %s"%(e))
            result[i] = None

    if full_run is True:
        return result

    return None