#!/usr/bin/python2

FRONTEND_IP="192.168.13.1"
CONTROLLER="192.168.13.1"
WORKERS=["worker1","worker2"]

import sys
sys.path.append("..")
import maxinet
from fatTree import FatTree
import time
import subprocess

topo = FatTree(4,10,0.1)

cluster = maxinet.Cluster(FRONTEND_IP, 9090, *WORKERS)
cluster.start()

exp = maxinet.Experiment(cluster, topo, controller=CONTROLLER)
exp.setup()

time.sleep(2)

h3 = exp.get_node("h3")
w3 = exp.find_worker("h3")

w3.run_cmd("dd if=/dev/urandom of=/tmp/testfile841203974 bs=1024 count=1024")
w3.get_file("/tmp/testfile841203974","/tmp/")
w3.put_file("/tmp/testfile841203974","/tmp/testfile415235977")
print w3.run_cmd("md5sum /tmp/testfile841203974").strip()
print w3.run_cmd("md5sum /tmp/testfile415235977").strip()
print subprocess.check_output(["md5sum","/tmp/testfile841203974"]).strip()
w3.run_cmd("rm /tmp/testfile841203974")
w3.run_cmd("rm /tmp/testfile415235977")
subprocess.call(["rm","/tmp/testfile841203974"])

time.sleep(2)

exp.stop()
