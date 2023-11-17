#!/usr/bin/env python3
import requests

print("[+] curi0usjack htaccess downloader")

for i in range(1,4):
    r=requests.get("https://gist.githubusercontent.com/curi0usJack/971385e8334e189d93a6cb4671238b10/raw/c1f61b6b2d43227d541f6f3cbf7bb874d8794c24/.htaccess")
    if r.status_code == 200:
        print("[+] Got .htaccess file!")
        break
    if i==3:
        print("[!] Failed to get htaccess file.")
        exit(2)
    print("[!] Getting htaccess failed(%i/3)")

contents=r.text
if contents[-1]=="\n":
    contents=contents[:-1]

f=open("sources/raw/curi0us-jack-htaccess","w")
f.write(contents)