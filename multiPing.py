#!/usr/bin/python2
FRONTEND_IP="192.168.126.146"
CONTROLLER="192.168.126.146"
WORKERS=["worker1","worker2"]

import sys
sys.path.append("..")
import maxinet
#import examples.topo as topo
import time
from fatTree import FatTree
from thinFT import thinFT
from Linear import Linear
from mininet.node import OVSSwitch, UserSwitch

#topo = thinFT(4,8000,0.0)
#topo = FatTree(4,8000,0.0)
topo = Linear(2,2,8000,0.0)
cluster = maxinet.Cluster(FRONTEND_IP, 9090, *WORKERS)
cluster.start()

exp = maxinet.Experiment(cluster, topo, controller=CONTROLLER, switch=OVSSwitch)
exp.setup()

print "waiting 3 seconds for routing algorithms on the controller to converge"
time.sleep(3)

print "Start test here"
print exp.get_node("h1").cmd("ping -c 15 10.0.0.2")
"""
time.sleep(2)
print exp.get_node("h3").cmd("iperf -s &")
print exp.get_node("h1").cmd("iperf -M 1400 -t 10 -c 10.0.0.3 > ~/results/iperf_h1.txt &")
print exp.get_node("h2").cmd("iperf -M 1400 -t 10 -c 10.0.0.3 > ~/results/iperf_h2.txt &")

print "wait for hosts to complete iperf"
time.sleep(15)
"""

exp.stop()
