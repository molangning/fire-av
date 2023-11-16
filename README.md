# Fire-AV
Fire-AV is a simple solution to your AV avoiding needs. Simply use the ips.txt file to begin blocking popular AV and cloud providers ips.

## Contribution
It is an arms race to discover AV provider IPs and I need help. If you find any ips that is not in the list please open an github issue so that I can add it.

## Usage
ips.txt should be integrated within the http server config(ie .htaccess) or updated dynamically by fetching the list and blocking at runtime. I do not recommend directly blocking these ip address through firewall programs like iptables as there may be cases where you need them to be accessible through a cloud service.

ips/user-agents that fits the blacklist should be served an normal webpage or an 404 page

# Files breakdown
sources/base-ips-ipv4.txt is a list of known av providers ip ranges(IPv4).
sources/aws-ips-ipv4.txt is a list of known aws ip ranges fetched daily(IPv4).

## Usage cases
> Your phishing domain keeps on getting flagged by AVs but you need them to complete the red team exercise
> The stager payload is hosted on a webpage and it is CRUCIAL for it to not get detected by the AVs

## Advisories
This list should only be used for red team exercises/engagements and should not be used for any nefarious purposes you have in mind.
IPv4 is currently supported, but IPv6 support is not supported and has no eta either