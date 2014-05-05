#!/usr/bin/python

import subprocess
import time
import os.path
import urllib2, urllib
import json

services = ['couchpotato', 'sickbeard', 'transmission-daemon']

def is_running_ps(process_name):
    proc1 = subprocess.Popen(['ps', 'aux'],stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', "%s" % process_name], stdin=proc1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=proc2.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
    proc2.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out,err=proc3.communicate()

    return out

    return bool(out.strip())

def is_running_service(service_name):
    proc = subprocess.Popen(['service', "%s" % service_name ,'status'],stdout=subprocess.PIPE)
    out,err=proc.communicate()

    return (proc.returncode == 0)

def is_xbmc_playing():
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request('http://localhost:8080/jsonrpc', '{"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}', headers)
    handler = urllib2.urlopen(request)
    j = json.loads(handler.read())

    return len(j["result"]) > 0

def stop_service(service_name):
    print "Stopping: %s" % service_name
    p = subprocess.Popen(['service', service_name, 'stop'],stdout=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        p2 = subprocess.Popen(['touch', "/tmp/.mc_%s" % service_name],stdout=subprocess.PIPE)

    print "Errorcode: %d" % p.returncode
    return p.returncode
    
def start_service(service_name):
    print "Starting: %s" % service_name
    p = subprocess.Popen(['service', service_name, 'start'],stdout=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        p2 = subprocess.Popen(['rm', '-f', "/tmp/.mc_%s" % service_name],stdout=subprocess.PIPE)

    print "Errorcode: %d" % p.returncode
    return p.returncode

def was_running(service_name):
    return os.path.isfile("/tmp/.mc_%s" % service_name)

def run():
    while True:
        for service in services:
            if is_xbmc_playing():
                if is_running_service(service):
                    stop_service(service)
            else:
                if was_running(service):
                    start_service(service)

        time.sleep(5)
if __name__ == "__main__":
    run()
