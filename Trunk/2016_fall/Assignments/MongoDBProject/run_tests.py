#!/usr/bin/env python

import os
import sys
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def parseStatus(status):
    data = {}
    status = status.strip()
    status = status.split("\n")
    data['code'] = status[0]
    
    for i in range(len(status)-1):
        if i == 0:
            continue
        d = status[i].split(":")
        data[d[0]] = d[1].strip()
    return data
    
def runCurl(ip,port,route):
    status = cmdline("curl -I -s -L http://"+ip+":"+port+route)
    status = parseStatus(status)

    
    if "200" in status['code']:
        return os.system("curl -X GET http://"+ip+":"+port+route)
    else:
        return status

ip = sys.argv[1]
port = sys.argv[2]

routes = [
"/city/city=Carnegie:start=0:limit=5",
"/closest/lon=-80.839186:lat=35.226504:start=0:limit=5",
"/reviews/id=hB3kH0NgM5LkEWMnMMDnHw:start=0:limit=5",
"/stars/id=hB3kH0NgM5LkEWMnMMDnHw:num_stars=5:start=0:limit=5",
"/yelping/min_years=5:start=0:limit=5",
"/most_likes/start=0:limit=5",
"/review_count/",
"/elite/start=0:limit=5",
"/elite/start=0:limit=1:sorted=reverse",
"/avg_elite/start=0:limit=5",
"/avg_elite/"
]

for route in routes:
    print("********************************************************")
    print(route)
    print(runCurl(ip,port,route))
    print("")
    print("********************************************************")
