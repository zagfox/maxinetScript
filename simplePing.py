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
from Linear import Linear
from mininet.node import OVSSwitch, UserSwitch

#topo = FatTree(4,10,0.1)
topo = Linear(2,1,10,0.0)
cluster = maxinet.Cluster(FRONTEND_IP, 9090, *WORKERS)
cluster.start()

exp = maxinet.Experiment(cluster, topo, controller=CONTROLLER, switch=OVSSwitch)
exp.setup()


#print exp.get_node("h1").cmd("ifconfig")
#print exp.get_node("h4").cmd("ifconfig")

print "waiting 5 seconds for routing algorithms on the controller to converge"
time.sleep(5)

print exp.get_node("h1").cmd("ping -c 5 10.0.0.4")
time.sleep(2)
print exp.get_node("h1").cmd("ping -c 5 10.0.0.2")


exp.stop()
