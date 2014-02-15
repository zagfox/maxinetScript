import sys, random,re
sys.path.append("..")

from partitioner import partitioner

from mininet.topo import Topo

class Linear(Topo):
    def randByte(self):
        return hex(random.randint(0,255))[2:]

    def makeMAC(self, i):
        return self.randByte()+":"+self.randByte()+":"+self.randByte()+":00:00:" + hex(i)[2:]
    
    def makeDPID(self, i):
        a = self.makeMAC(i)
        dp = "".join(re.findall(r'[a-f0-9]+',a))
        return "0" * ( 12 - len(dp)) + dp
    
    # args is a string defining the arguments of the topology! has be to format: "x,y,z" to have x hosts and a bw limit of y for those hosts each and a latency of z (in ms) per hop
    def __init__(self, k=2, n=1, bwlimit=10, lat=0.1, **opts):
        "Linear topology of k switches, with n hosts per switch."

        Topo.__init__(self, **opts)
        self.k = k
	self.n = n

        """
	if n == 1:
	    getHostName = lambda i, j: 'h%s' % i
	else:
	    getHostName = lambda i, j: 'h%ss%d' % (j, i)
	"""

        lastSwitch = None
	for i in range(k):
	    # Add switch
            switch = self.addSwitch('s' + str(i+1), dpid=self.makeDPID(i+1),  
	        **dict(listenPort=(13000+i)))
	    # Add hosts
	    for j in range(n):
                host = self.addHost('h'+str(i*n+j+1), #getHostName(i+1,j+1),
		    mac=self.makeMAC(j+1), ip="10.0.0." + str(i*n+j+1))
                self.addLink(host, switch, bw=bwlimit, delay=str(lat) + "ms")
            if lastSwitch:
                self.addLink(switch, lastSwitch, bw=bwlimit, delay=str(lat) + "ms")
	    lastSwitch = switch





