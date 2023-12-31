# Fire-AV
Fire-AV is a simple solution to your AV avoiding needs. Simply use the ips.txt file to begin blocking popular AV and cloud providers ips.

## Status
Fire-AV is now in its stable stage! Changes may still be added to `asn-list.json` and formatting may change overtime(but less frequently)

## Contribution
It is an arms race to discover AV provider IPs and I need help. If you find any ips that is not in the list please open an github issue so that I can add it.

## Usage
I do not recommend directly using the lists provided unless you are willing to do a lot of trial and errors. Instead, You are encouraged to build your own filter list to tailor it to your needs/infrastructure

The blocklists should be integrated within the http server config(ie .htaccess) or updated dynamically by fetching the list and blocking at runtime. 

ips/user-agents that fits the blacklist should be served an normal webpage or an 404 page

## Directory structure breakdown

### Sources files
|   directory path  |      Description      |
| ----------------- | --------------------- |
| [sources/ips](sources/ips) | Directory containing a list of ips |
| [sources/user-agents](sources/user-agents) | Directory containing a list of User agents |

The `regexps` directory in `sources/user-agents` contains regexps rules to match common bots. All regexps are in javascript format so you need to parse them.

### Blacklists
|     File path     |      Description      |
| ----------------- | --------------------- |
| [blacklists/blacklists-ips-ipv4.txt](blacklists/blacklists-ips-ipv4.txt) | Compiled ip ranges from the sources files |
| [blacklists/blacklists-ips-dangerous-ipv4.txt](blacklists/blacklists-ips-dangerous-ipv4.txt) | Compiled ip ranges from the sources files that may break your program |
| [blacklists/blacklists-user-agent.txt](blacklists/blacklists-user-agents.txt) | Compiled user agents from the sources files |

### Whitelists
|     File path     |      Description      |
| ----------------- | --------------------- |
| [whitelists/whitelists-ips-ipv4.txt](whitelists/whitelists-ips-ipv4.txt) | Compiled ip ranges from the sources files |
| [whitelists/whitelists-ips-ipv4.txt](whitelists/whitelists-user-agents.txt) | Compiled ip ranges from the sources files |

## Usage cases
- Your phishing domain keeps on getting flagged by AVs but you need them to complete the red team exercise
- The stager payload is hosted on a webpage and it is CRUCIAL for it to not get detected by the AVs

## Advisories
This list should only be used for red team exercises/engagements and should not be used for any nefarious purposes you have in mind.
IPv4 is currently supported, but IPv6 support is not supported and has no eta either

## TODOs
- [ ] IP range "collapser", bunches up ip address using cidr notation.