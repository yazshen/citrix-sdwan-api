import sys, os, ssl, http.client, json

"""

Author: Robbie Shen
Date: 2020.01.22
Contact: yazhong.shen@citrix.com

TODO: add-static-route-V1.py <MCN address> <UserName> <UserPassword> <Package Name> <Site Name> <Static Route File Name> <Static Route Cost> <Static Route Gateway>

Requirements: Python 3.7.6 or higher

"""



def main() :
    varMCN = sys.argv[1]
    varUsr = sys.argv[2]
    varPwd = sys.argv[3]
    varPkg = sys.argv[4]
    varSite = sys.argv[5]
    varFile = sys.argv[6]
    varRouteCost = sys.argv[7]
    varRouteGW = sys.argv[8]
    if not os.path.isfile(varFile):
        print("Static Route File {} does not exist. Exiting..." . format(varFile))
        sys.exit()
    i = 0
    arrRoutes = {}
    print("Loading Routes from file...")
    with open(varFile) as fp:
        line = fp.readline()
        while line:
            arrRoutes[i] = line.replace('\n','')
            line = fp.readline()
            i += 1
    fp.close()
    print("Routes successfully loaded.")
    #print(len(arrRoutes))


    print("Login to Citrix SD-WAN MCN: {}" . format(varMCN))
    https_headers = {"Content-type": "application/json"}
    https_params = json.dumps({'login':{'username':varUsr,'password':varPwd,'timeout':'9999'}})
    #print(https_params)

    https_conn = http.client.HTTPSConnection(varMCN, context = ssl._create_unverified_context())
    https_conn.request("POST", "/sdwan/nitro/v1/config/login", https_params, https_headers)
    https_response = https_conn.getresponse()
    if https_response.status != 200:
        print("Failed to login to Citrix SD-WAN, Reason is: " + https_response.reason)
        sys.exit()
    print("Successfully login to Citrix SD-WAN.")

    #print(https_response.read())
    #print(https_response.headers)
    https_response_cookie = https_response.getheader('Set-Cookie').split(';')[0]
    #print(https_response_cookie)

    i = 0
    while i <= (len(arrRoutes) -1):
        https_params = json.dumps({'routes': {'cost':varRouteCost,'gateway_ip_addr':varRouteGW,'service_type':'local','network_ip_address':arrRoutes[i],'site_name':varSite,'package_name':varPkg}})
        #print(https_params)

        try:
            https_conn = http.client.HTTPSConnection(varMCN, timeout=15, context=ssl._create_unverified_context())
            https_headers = {"Content-type": "application/json","Cookie": https_response_cookie}
            #print(https_headers)
            https_conn.request("POST", "/sdwan/nitro/v1/config_editor/routes/package_name=" + varPkg, https_params, https_headers)
            https_response = https_conn.getresponse()
            #print(https_response.read())
            if https_response.status != 200:
                print(str(i+1) + ": " + arrRoutes[i] + " Failed to write static route. Reason is: " + https_response.reason)
            else:
                print(str(i+1) + ": " + arrRoutes[i] + " " + json.loads(https_response.read().decode("utf-8"))['routes']['message'])
        except Exception as e:
            print(str(i+1) + ": " + arrRoutes[i] + " Exception::message is: " + str(e.args))

        https_conn.close()
        i += 1

    print("All Done!")


if __name__ == '__main__':
    #print(sys.argv)
    #print(len(sys.argv))
    if len(sys.argv) != 9:
        print("Usage: add-static-route-V1.py <MCN address> <UserName> <UserPassword> <Package Name> <Site Name> <Static Route File Name> <Static Route Cost> <Static Route Gateway>")
        sys.exit()
    else:
        main()
