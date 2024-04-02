#!/usr/bin/env python3

import os
import time
import random
import hashlib
import tarfile
import zipfile
import requests

COMPRESSED_BASE_PATH = "sources/raw/maxmind-compressed/"
UNCOMPRESSED_BASE_PATH = "sources/raw/maxmind-geolite-db/"
BAD_CHARS = {"/", "\\"}

hash_url = ".sha256"
urls = [
    "https://download.maxmind.com/geoip/databases/GeoLite2-ASN/download?suffix=tar.gz",
    "https://download.maxmind.com/geoip/databases/GeoLite2-ASN-CSV/download?suffix=zip",
    "https://download.maxmind.com/geoip/databases/GeoLite2-City/download?suffix=tar.gz",
    "https://download.maxmind.com/geoip/databases/GeoLite2-City-CSV/download?suffix=zip",
    "https://download.maxmind.com/geoip/databases/GeoLite2-Country/download?suffix=tar.gz",
    "https://download.maxmind.com/geoip/databases/GeoLite2-Country-CSV/download?suffix=zip"
]
urls = random.sample(urls, len(urls))

if "MAXMIND_AUTH_DETAILS" not in os.environ:
    print("[!] Maxmind key not found!")
    exit(2)

maxmind_auth = os.environ["MAXMIND_AUTH_DETAILS"]
session = requests.Session()
session.auth = tuple(maxmind_auth.split(":", 1))

def check_fresh():
    if session.head(urls[0]).status_code == 200:
        return True
    
    return False

def check_bad_filename(filename):
    return bool(set(filename).intersection(BAD_CHARS))

def downloader(url, output_location):
    resp = session.head(url)

    if "Content-Disposition" not in resp.headers:
        print("[-] Content-Disposition header not found!")

    print(f"[+] Started downloading file {output_location.split('/')[-1]}")

    with session.get(url) as r:
        with open(output_location, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("[+] Finished downloading file")

def create_if_not_exists(path):

    if not os.path.isdir(path):
        print(f"[!] Directory {path.split('/')[-1]} not created, creating it now")
        os.makedirs(path)

def download_all():

    file_locations = []

    for i in urls:
        resp = session.get(i + hash_url)

        if resp.status_code != 200:
            print(f"[-] Maxmind returned {resp.status_code} instead of 200")
            continue

        filename = resp.headers["Content-Disposition"].split("filename=", 1)[-1].split(".sha256", 1)[0]

        if check_bad_filename(filename):
            print(f"[!] Maxmind gave us a filename with a slash ({filename})")
            exit(2)

        file_location = os.path.join(COMPRESSED_BASE_PATH, "latest", filename)

        if os.path.isfile(file_location) and hashlib.sha256(open(file_location, "rb").read()).hexdigest() == resp.content.split(b" ")[0].strip().decode():
            print(f"[+] {filename} exists and hash matches.")
            time.sleep(0.2)
            continue

        create_if_not_exists(os.path.join(COMPRESSED_BASE_PATH, "latest"))
        file_locations.append(file_location)
        downloader(i, file_location)
        
        time.sleep(0.5)

    create_if_not_exists(os.path.join(COMPRESSED_BASE_PATH, "latest"))

    for file in file_locations:
        if file.endswith(".zip"):
            
            zip = zipfile.ZipFile(file)
            for zipped_file in zip.infolist():
                if zipped_file.filename.endswith(".txt"):
                    continue

                output_dir = zipped_file.filename.split("/")[0].split("_")[0]
                
                if check_bad_filename(output_dir):
                    print(f"[!] Maxmind gave us a zip file with a slash ({output_dir})")
                    break

                output_dir = os.path.join(UNCOMPRESSED_BASE_PATH, "latest", output_dir)
                create_if_not_exists(output_dir)
                zip.extract(zipped_file.filename, output_dir)

            else:
                print(f"[+] Finished processing {file.split('/')[-1]}")

        elif file.endswith(".tar.gz"):
            
            gzip = tarfile.open(file)
            for gzipped_file in gzip.getnames():
                if gzipped_file.endswith(".txt") or "/" not in gzipped_file:
                    continue

                output_dir = gzipped_file.split("/")[0].split("_")[0]

                if check_bad_filename(output_dir):
                    print(f"[!] Maxmind gave us a gunzipped file with a slash ({output_dir})")
                    break

                output_dir = os.path.join(UNCOMPRESSED_BASE_PATH, "latest", output_dir)
                create_if_not_exists(output_dir)
                gzip.extract(gzipped_file, output_dir, filter="data")
            
            else:
                print(f"[+] Finished processing {file.split('/')[-1]}")

        else:
            print(f"[!] Unknown file {file}")
    

if not check_fresh():
    print("Login is invalid")
    exit(2)

print("Login is valid")

download_all()

