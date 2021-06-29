# Citrix SD-WAN API Guide
![Citrix SD-WAN](https://www.citrix.com/content/dam/citrix61/en_us/images/graphics/infographics/sd-wan-diagram.png)

## 1. Batch import static routes into SD-WAN Site
https://github.com/yazshen/citrix-sdwan-api/blob/master/add-static-route-V1.py

### API Version
Citrix SD-WAN NITRO REST API V1

### Usage
add-static-route-V1.py \<MCN address\> \<UserName\> \<UserPassword\> \<Package Name\> \<Site Name\> \<Static Route File Name\> \<Static Route Cost\> \<Static Route Gateway\>

### Example
add-static-route-V1.py 192.168.100.1 admin password 20200121-yazhongs Shanghai-Office test.txt 5 192.168.1.1

### Requirements
Python 3.7.6 or higher

## 2.Monitor AliCloud Route Table when using Citrix SD-WAN Active-Active scenario
https://github.com/yazshen/citrix-sdwan-api/blob/master/monitor-sdwan-alicloud.py

### TODO
Monitor Route Table on AliCloud when using Citrix SD-WAN Active-Active Scenario. If Primary SD-WAN Appliance down, update Next-Hop to Secondary SD-WAN Appliance. 

### Prerequisite
AccessKey on AliCloud requires "AliyunVPCFullAccess"

### Requirements
Python 3.6.8 or higher

## License
GNU General Public License v3.0
(https://github.com/yazshen/citrix-sdwan-api/blob/master/LICENSE)
