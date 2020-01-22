# Citrix SD-WAN API Guide

## Batch import static routes into SD-WAN Site
https://github.com/yazshen/citrix-sdwan-api/blob/master/add-static-route-V1.py

### API Version
Citrix SD-WAN API V1

### Usage
add-static-route-V1.py \<MCN address\> \<UserName\> \<UserPassword\> \<Package Name\> \<Site Name\> \<Static Route File Name\> \<Static Route Cost\> \<Static Route Gateway\>

### Example
add-static-route-V1.py 192.168.100.1 admin password 20200121-yazhongs Shanghai-Office test.txt 5 192.168.1.1

### Requirements
Python 3.7.6 or higher


## License
GNU General Public License v3.0
(https://github.com/yazshen/citrix-sdwan-api/blob/master/LICENSE)
