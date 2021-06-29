#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import platform
import subprocess
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkvpc.request.v20160428.DescribeRouteEntryListRequest import DescribeRouteEntryListRequest
from aliyunsdkcore.request import CommonRequest
from aliyunsdkvpc.request.v20160428.DeleteRouteEntryRequest import DeleteRouteEntryRequest

"""

Author: Robbie Shen
Date: 2021.06.29
Contact: yazhong.shen@citrix.com

TODO: Monitor Route Table on AliCloud when using Citrix SD-WAN Active-Active Scenario. If Primary SD-WAN Appliance down, update Next-Hop to Secondary SD-WAN Appliance. 

Prerequisite: AccessKey on AliCloud requires "AliyunVPCFullAccess"

Requirements: Python 3.6.8 or higher

"""


var_ALI_AccessKey = '<Your AliCloud Access Key>'
var_ALI_AccessSecret = '<Your AliCloud Access Secret>'
var_ALI_Region = 'cn-shanghai'
var_ALI_RouteTableID = '<Your Route Table ID>'
var_ALI_RouteEntryName = "shanghai-lab"
var_ALI_Pri_NextHopID = '<Your Primary ECS NIC ID>'
var_ALI_Sec_NextHopID = '<Your Secondary ECS NIC ID>'
var_ALI_DestinationCidrBlock = '192.168.50.0/24'
var_SDWAN_Pri_VIP = '192.168.21.100'



def fun_ping_server(host, network_timeout=3):
    args = [
        'ping'
    ]

    platform_os = platform.system().lower()

    if platform_os == 'windows':
        args.extend(['-n', '1'])
        args.extend(['-w', str(network_timeout * 1000)])
    elif platform_os in ('linux', 'darwin'):
        args.extend(['-c', '1'])
        args.extend(['-W', str(network_timeout)])
    else:
        raise NotImplemented('Unsupported OS: {}'.format(platform_os))

    args.append(host)

    try:
        if platform_os == 'windows':
            output = subprocess.run(args, check=True, universal_newlines=True).stdout

            if output and 'TTL' not in output:
                return False
        else:
            subprocess.run(args, check=True)

        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def fun_ali_check_primary_route():
    client = AcsClient(var_ALI_AccessKey, var_ALI_AccessSecret, var_ALI_Region)

    request = DescribeRouteEntryListRequest()
    request.set_accept_format('json')
    request.set_RouteTableId(var_ALI_RouteTableID)

    try:
        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
        if str(response, encoding='utf-8').find(var_ALI_DestinationCidrBlock) == -1:
            return True
        else:
            if str(response, encoding='utf-8').find('RouteEntryName":"' + var_ALI_RouteEntryName + '","NextHops":{"NextHop":[{"NextHopType":"NetworkInterface","NextHopId":"' + var_ALI_Pri_NextHopID) > -1:
                return True
            else:
                return False
    except:
        return True

def fun_ali_switch_sdwan_route(currentNextHopID,newNextHopID):
    client = AcsClient(var_ALI_AccessKey, var_ALI_AccessSecret, var_ALI_Region)

    request1 = DeleteRouteEntryRequest()
    request1.set_accept_format('json')
    request1.set_RouteTableId(var_ALI_RouteTableID)
    request1.set_NextHopId(currentNextHopID)
    request1.set_DestinationCidrBlock(var_ALI_DestinationCidrBlock)

    try:
        response1 = client.do_action_with_exception(request1)
        print(str(response1, encoding='utf-8'))
        requestStatus = True
    except:
        requestStatus = False

    if requestStatus == True:
        """
        request2 = CreateRouteTableRequest()
        request2.set_accept_format('json')
        request2.set_RouteTableId(var_ALI_RouteTableID)
        request2.set_DestinationCidrBlock(var_ALI_DestinationCidrBlock)
        request2.set_NextHopId(newNextHopID)
        request2.set_NextHopType('NetworkInterface')

        time.sleep(5)
        response2 = client.do_action_with_exception(request2)
        #print(str(response2, encoding='utf-8'))
        """
        request2 = CommonRequest()
        request2.set_accept_format('json')
        request2.set_domain('vpc.aliyuncs.com')
        request2.set_method('POST')
        request2.set_protocol_type('https')  # https | http
        request2.set_version('2016-04-28')
        request2.set_action_name('CreateRouteEntry')

        request2.add_query_param('RouteTableId', var_ALI_RouteTableID)
        request2.add_query_param('RouteEntryName', var_ALI_RouteEntryName)
        request2.add_query_param('DestinationCidrBlock', var_ALI_DestinationCidrBlock)
        request2.add_query_param('NextHopType', "NetworkInterface")
        request2.add_query_param('NextHopId', newNextHopID)

        time.sleep(6)
        response2 = client.do_action_with_exception(request2)
        print(str(response2, encoding='utf-8'))

        return True
    else:
        return False

if __name__ == '__main__':
    while 1 == 1:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : Route Table Checking...")
        if fun_ping_server(var_SDWAN_Pri_VIP,1) == True:
            if fun_ali_check_primary_route() == False:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : Switching Route Table to Primary SD-WAN")
                fun_ali_switch_sdwan_route(var_ALI_Sec_NextHopID,var_ALI_Pri_NextHopID)
        else:
            if fun_ali_check_primary_route() == True:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " : Switching Route Table to Secondary SD-WAN")
                fun_ali_switch_sdwan_route(var_ALI_Pri_NextHopID,var_ALI_Sec_NextHopID)
        time.sleep(10)
