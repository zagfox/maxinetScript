#!/usr/bin/python2
"""
traffic.py: test different traffic patterns for link
"""

import os
import sys
sys.path.append("..")
import maxinet
import time
from thinFT import thinFT
from Linear import Linear
from mininet.node import OVSSwitch, UserSwitch

def trafficTest(srcNum, dstNum, exp, seconds ):
	print "Start %d, %d traffic test here" %(srcNum, dstNum)
	resultPath = "/home/maxinet/maxinet/Frontend/maxinetScript/Results/%d%dtraffic/" %(srcNum, dstNum)
	if not os.path.exists(resultPath): os.makedirs(resultPath)
	for i in range(dstNum):
		exp.get_node("h"+str(i+5)).cmd("iperf -s &")
	iperfCmd = "iperf -M 1400 -t %d -c 10.0.0." %seconds
	if dstNum is 1:
		for i in range(srcNum):
			exp.get_node("h"+str(i+1)).cmd(iperfCmd+"5"+" > "+resultPath+"iperf_h%d.txt &" % (i+1))
	else:
		for i in range(dstNum):
			exp.get_node("h"+str(i+1)).cmd(iperfCmd+str(i+5)+" > "+resultPath+"iperf_h%d.txt &" % (i+1))

	print "wait for hosts to complete iperf"
	time.sleep(seconds+5)

def bi_trafficTest(srcNum, dstNum, exp, seconds ):
	print "Start bi %d, %d traffic test here" %(srcNum, dstNum)
	resultPath = "/home/maxinet/maxinet/Frontend/maxinetScript/Results/bi%d%dtraffic/" %(srcNum, dstNum)
	if not os.path.exists(resultPath): os.makedirs(resultPath)
	for i in range(8):
		exp.get_node("h"+str(i+1)).cmd("iperf -s &")
	iperfCmd = "iperf -M 1400 -t %d -c 10.0.0." %seconds
	if dstNum is 1:
		for i in range(srcNum):
			exp.get_node("h"+str(i+1)).cmd(iperfCmd+"5"+" > "+resultPath+"iperf_h%d.txt &" % (i+1))
			#exp.get_node("h"+str(i+5)).cmd(iperfCmd+"1"+" > "+resultPath+"iperf_h%d.txt &" % (i+5))
	"""
	else:
		for i in range(dstNum):
			exp.get_node("h"+str(i+1)).cmd(iperfCmd+str(i+5)+" > "+resultPath+"iperf_h%d.txt &" % (i+1))
	"""

	print "wait for hosts to complete iperf"
	time.sleep(seconds+5)



if __name__ == '__main__':
	FRONTEND_IP="192.168.126.146"
	CONTROLLER="192.168.126.146"
	WORKERS=["worker1"]#,"worker2"]

	#topo = thinFT(4,8000,0.0)
	#topo = FatTree(4,8000,0.0)
	topo = Linear(2,4,100,0.0)
	cluster = maxinet.Cluster(FRONTEND_IP, 9090, *WORKERS)
	cluster.start()

	exp = maxinet.Experiment(cluster, topo, controller=CONTROLLER, switch=OVSSwitch)
	exp.setup()

	print "waiting 3 seconds for routing algorithms on the controller to converge"
	time.sleep(3)

	#trafficTest(1, 1, exp, 20)
	bi_trafficTest(1, 1, exp, 20)
	#trafficTest(4, 1, exp, 20)
	#trafficTest(4, 4, exp, 20)

	exp.stop()
