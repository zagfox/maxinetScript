import sys, random,re
sys.path.append("..")

from partitioner import partitioner

from mininet.topo import Topo

class treetopo(Topo):
    def randByte(self):
        return hex(random.randint(0,255))[2:]

    def makeMAC(self, i):
        return self.randByte()+":"+self.randByte()+":"+self.randByte()+":00:00:" + hex(i)[2:]
    
    def makeDPID(self, i):
        a = self.makeMAC(i)
        dp = "".join(re.findall(r'[a-f0-9]+',a))
        return "0" * ( 12 - len(dp)) + dp
    
    def addTree(self, depth, fanout, bwlimit, lat):
        isSwitch = depth>0
        if isSwitch:
            node = self.addSwitch('s'+str(self.switchNum), dpid=self.makeDPID(self.switchNum),\
	        **dict(listenPort=(13000+self.switchNum-1)))
	    self.switchNum += 1
	    for _ in range( fanout ):
	        child = self.addTree(depth-1, fanout, bwlimit, lat)
		self.addLink(child, node, bw=bwlimit, delay=str(lat)+"ms")
	else:
            node = self.addHost('h' + str(self.hostNum), mac=self.makeMAC(self.hostNum), \
	        ip="10.0.0." + str(self.hostNum))
	    self.hostNum += 1
	return node

    # args is a string defining the arguments of the topology! has be to format: 
    #"x,y,z" to have x hosts and a bw limit of y for those hosts each and a latency of z (in ms) per hop
    def __init__(self, depth=1, fanout=2, bwlimit=1000, lat=0.0, **opts):
        Topo.__init__(self, **opts)
	"""
        self.hostNum = 1
        self.switchNum = 1
        self.addTree(depth, fanout,bwlimit, lat)
	"""
 
        tor = []

        numLeafes = fanout**depth
        bw = bwlimit

        s = 1
        #bw = 10

        for i in range(0, numLeafes, fanout):
            sw = self.addSwitch('s' + str(s), dpid=self.makeDPID(s),  **dict(listenPort=(13000+s-1)))
            s = s+1
	    for j in range(fanout):
                h = self.addHost('h' + str(i+j+1), mac=self.makeMAC(i+j+1), ip="10.0.0." + str(i+j+1))
                self.addLink(h, sw, bw=bw, delay=str(lat) + "ms")
            tor.append(sw)

        toDo = tor  # nodes that have to be integrated into the tree

        while len(toDo) > 1:
            newToDo = []
            for i in range(0, len(toDo), fanout):
                sw = self.addSwitch('s' + str(s), dpid=self.makeDPID(s), **dict(listenPort=(13000+s-1)))
                s = s+1
                newToDo.append(sw)
         	for j in range(fanout):
		    if i+j < len(toDo):
                        self.addLink(toDo[i+j], sw, bw=bw, delay=str(lat) + "ms")
            toDo = newToDo
            bw = fanout*bw
            
                    
