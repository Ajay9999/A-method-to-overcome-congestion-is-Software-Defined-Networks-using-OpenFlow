from mininet.topo import Topo
from mininet.node import Node
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from mininet.log import setLogLevel

from mininet.link import Link, TCLink
import json, requests;
import thread
# from threading import Thread
import time
import os


class LinuxRouter( Node ):
    	"A Node with IP forwarding enabled."
	def config( self, **params ):
        	super( LinuxRouter, self).config( **params )
        	# Enable forwarding on the router
        	self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
	        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
	        super( LinuxRouter, self ).terminate()

class MyTopo( Topo ):

	def __init__( self ):
		Topo.__init__( self )

		net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )

 		router = self.addNode( 'r0',cls=LinuxRouter,ip="10.1.1.1/24")

        	# Add hosts and switches

	        h1 = net.addHost( 'h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01" )
	        h2 = net.addHost( 'h2', ip="10.0.1.20/24", mac="00:00:00:00:00:02" )
 	        h3 = net.addHost( 'h3', ip="10.0.3.10/24", mac="00:00:00:00:00:03" )
        	h4 = net.addHost( 'h4', ip="10.0.3.20/24", mac="00:00:00:00:00:04" )
		h5 = net.addHost( 'h5', ip="10.0.4.10/24", mac="00:00:00:00:00:05" )
		h6 = net.addHost( 'h6', ip="10.0.4.20/24", mac="00:00:00:00:00:06" )
 	        h7 = net.addHost( 'h7', ip="10.0.5.10/24", mac="00:00:00:00:00:07" )
        	h8 = net.addHost( 'h8', ip="10.0.5.20/24", mac="00:00:00:00:00:08" )

        	r1 = net.addHost( 'r1')
		r2 = net.addHost( 'r2')

        	s1 = net.addSwitch( 's1')
        	s2 = net.addSwitch( 's2')
		s3 = net.addSwitch( 's3')
		s4 = net.addSwitch( 's4')
		s5 = net.addSwitch( 's5')
        	s6 = net.addSwitch( 's6')
		s7 = net.addSwitch( 's7')
		s8 = net.addSwitch( 's8')
 
		c0 = net.addController( 'c0', controller=RemoteController, ip='0.0.0.0', port=6653 )
 

        	net.addLink( r1, s1, bw=10, max_queue_size=1000 )
        	net.addLink( r1, s2, bw=10, max_queue_size=1000)
		net.addLink( r1, s5, bw=5, max_queue_size=1000 )
        	net.addLink( r1, s6, bw=5, max_queue_size=1000 )
		net.addLink( r2, s1, bw=5, max_queue_size=1000 )
        	net.addLink( r2, s2, bw=5, max_queue_size=1000)
		net.addLink( r2, s5, bw=5, max_queue_size=1000 )
        	net.addLink( r2, s6, bw=5, max_queue_size=1000 )

        	net.addLink( h1, s3, bw=20, max_queue_size=1000)	
        	net.addLink( h2, s3, bw=20, max_queue_size=1000)
        	net.addLink( h3, s4, bw=20, max_queue_size=1000)
        	net.addLink( h4, s4, bw=20, max_queue_size=1000)
		net.addLink( h5, s7, bw=20, max_queue_size=1000)
        	net.addLink( h6, s7, bw=20, max_queue_size=1000)
		net.addLink( h7, s8, bw=20, max_queue_size=1000)
        	net.addLink( h8, s8, bw=20, max_queue_size=1000)

		net.addLink( s1,s3, bw=5, max_queue_size=1000)
		net.addLink( s1,s4, bw=5, max_queue_size=1000)
		net.addLink( s2,s3, bw=5, max_queue_size=1000)
		net.addLink( s3,s4, bw=5, max_queue_size=1000)
		net.addLink( s2,s4, bw=15, max_queue_size=1000)
		net.addLink( s1,s2, bw=5, max_queue_size=1000)
		net.addLink( s5,s7, bw=5, max_queue_size=1000)
		net.addLink( s5,s6, bw=5, max_queue_size=1000)
		net.addLink( s5,s8, bw=5, max_queue_size=1000)
		net.addLink( s6,s7, bw=5, max_queue_size=1000)
		net.addLink( s6,s8, bw=5, max_queue_size=1000)
		net.addLink( s7,s8, bw=5, max_queue_size=1000)
		"""net.addLink( r1,s1 )
		net.addLink( r1,s2 )
		net.addLink( r1,s5 )
		net.addLink( r1,s6 )"""

        	net.build()
		c0.start()

        	s1.start( [c0] )
        	s2.start( [c0] )
		s3.start( [c0] )
        	s4.start( [c0] )
		s5.start( [c0] )
        	s6.start( [c0] )
		s7.start( [c0] )
        	s8.start( [c0] )
		

        	r1.cmd("ifconfig r1-eth0 0")
        	r1.cmd("ifconfig r1-eth1 0")
		r1.cmd("ifconfig r1-eth2 0")
        	r1.cmd("ifconfig r1-eth3 0")
		r2.cmd("ifconfig r2-eth0 0")
        	r2.cmd("ifconfig r2-eth1 0")
		r2.cmd("ifconfig r2-eth2 0")
        	r2.cmd("ifconfig r2-eth3 0")
		

        	r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")
        	r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:02")
		r1.cmd("ifconfig r1-eth2 hw ether 00:00:00:00:01:03")
        	r1.cmd("ifconfig r1-eth3 hw ether 00:00:00:00:01:04")
		r2.cmd("ifconfig r2-eth0 hw ether 00:00:00:00:01:05")
        	r2.cmd("ifconfig r2-eth1 hw ether 00:00:00:00:01:06")
		r2.cmd("ifconfig r2-eth2 hw ether 00:00:00:00:01:07")
        	r2.cmd("ifconfig r2-eth3 hw ether 00:00:00:00:01:08")

        	r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")
        	r1.cmd("ip addr add 10.0.3.1/24 brd + dev r1-eth1")
		r1.cmd("ip addr add 10.0.4.1/24 brd + dev r1-eth2")
        	r1.cmd("ip addr add 10.0.5.1/24 brd + dev r1-eth3")
		r2.cmd("ip addr add 10.0.1.2/24 brd + dev r2-eth0")
        	r2.cmd("ip addr add 10.0.3.2/24 brd + dev r2-eth1")
		r2.cmd("ip addr add 10.0.4.2/24 brd + dev r2-eth2")
        	r2.cmd("ip addr add 10.0.5.2/24 brd + dev r2-eth3")

        	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
		r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

        	h1.cmd("ip route add default via 10.0.1.1")
        	h2.cmd("ip route add default via 10.0.1.1")

        	h3.cmd("ip route add default via 10.0.3.1")
        	h4.cmd("ip route add default via 10.0.3.1")

		h5.cmd("ip route add default via 10.0.4.2")
        	h6.cmd("ip route add default via 10.0.4.2")

        	h7.cmd("ip route add default via 10.0.5.2")
        	h8.cmd("ip route add default via 10.0.5.2")


        		#OLD FLOWS
        		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"h10s31", "priority":"1", "eth_src": "00:00:00:00:00:01","actions":"output=4"}')
            	# if flag == 0:	
            		# print "IN OLD"
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f", "priority":"1", "eth_src": "00:00:00:00:00:01","actions":"output=3"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f2", "priority":"1", "eth_src": "00:00:00:00:00:02","actions":"output=3"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f3", "priority":"1", "eth_dst": "00:00:00:00:00:01","actions":"output=1"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f4", "priority":"1", "eth_dst": "00:00:00:00:00:02","actions":"output=2"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f5", "priority":"1", "in_port" : "3","actions":"output=1"}')
		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f12", "priority":"1", "in_port" : "5","actions":"output=1"}')
		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f13", "priority":"1", "eth_dst" : "00:00:00:00:00:02","actions":"output=5"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f6", "priority":"1", "in_port" : "1","actions":"output=3"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f7", "priority":"1", "in_port" : "1","actions":"output=4"}')
		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f11", "priority":"1", "in_port" : "3","actions":"output=5"}')
		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f13", "priority":"1", "in_port" : "5","actions":"output=3"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f8", "priority":"1", "in_port" : "4","actions":"output=1"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"f9", "priority":"1", "in_port" : "5","actions":"output=2"}')
		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"f10", "priority":"1", "in_port" : "2","actions":"output=5"}')





        		##NEW FLOWS

        	# if flag == 1:
        		
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f9", "priority":"1", "eth_dst": "00:00:00:00:00:01","actions":"output=1"}')
 
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f10", "priority":"1", "eth_dst": "00:00:00:00:00:02","actions":"output=2"}')
       
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f12", "priority":"1", "in_port" : "5","actions":"output=1"}')
       
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f11", "priority":"1", "in_port" : "3","actions":"output=5"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f13", "priority":"1", "in_port" : "5","actions":"output=3"}')
        	
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f14", "priority":"1", "eth_dst": "00:00:00:00:00:02","actions":"output=4"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f15", "priority":"1", "eth_dst": "00:00:00:00:00:01","actions":"output=3"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f1", "priority":"1", "eth_src": "00:00:00:00:00:01","actions":"output=3"}')
        	
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"f2", "priority":"1", "eth_src": "00:00:00:00:00:02","actions":"output=4"}') 
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f3", "priority":"1", "in_port": "3","actions":"output=1"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f4", "priority":"1", "in_port": "1","actions":"output=4"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"f5", "priority":"1", "in_port": "5","actions":"output=2"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"f20", "priority":"1", "in_port": "3","actions":"output=4"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"f6", "priority":"1", "in_port": "2","actions":"output=5"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"f7", "priority":"1", "in_port": "4","actions":"output=1"}')
        	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"f8", "priority":"1", "in_port": "1","actions":"output=3"}')


            	

     		# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"s11r10", "priority":"1", "ethtype":"0x0800","ipv4_dst":"10.0.3.*","actions":"output=1"}')  
            	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"s21r11", "priority":"1", "ethtype":"0x0800","ipv4_dst":"10.0.1.*","actions":"output=1"}')       	
            	req_get_switch_details = requests.get('http://127.0.0.1:8080/wm/staticflowpusher/list/00:00:00:00:00:00:00:03/json')
            	switch_details_json = json.loads(req_get_switch_details.text)
            	print switch_details_json
        	print "*** Running CLI"
        	# b=dijkstra(graph,'s3','s1')
		# b = list(reversed(a))
		# print b
		# cal_flows(switch, graph1,b)
		# h1.cmd("iperf -s -u")
		i = 0
		# while i < 5:
		# # 	h2.cmd("iperf -c -u 10.0.1.10 -b 10M -t 10")
		# 	os.system("ovs-ofctl dump-ports s1 >> outpit.txt")
		# 	i += 1
		# 	time.sleep(5)

		# h1.cmd("iperf -s -u")
		# h2.cmd("iperf -c -u 10.0.1.10 -b 10M -t 10")
        	CLI( net )

		# thread.join()
                # print arr
		print "YESS"
        	print "*** Stopping network"

        	net.stop()

a=[]
def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    """ calculates a shortest path tree routed in src
    """    
    # a few sanity checks
    if src not in graph:
        raise TypeError('The root of the shortest path tree cannot be found')
    if dest not in graph:
        raise TypeError('The target of the shortest path cannot be found')    
    # ending condition
    if src == dest:
        # We build the shortest path and display it
        path=[]
        pred=dest
        while pred != None:
            path.append(pred)
            a.append(pred)
            pred=predecessors.get(pred,None)
        print('shortest path: '+str(path)+" cost="+str(distances[dest]))
    else :     
        # if it is the initial  run, initializes the cost
        if not visited: 
            distances[src]=0
        # visit the neighbors
        for neighbor in graph[src] :
            if neighbor not in visited:
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        # mark as visited
        visited.append(src)
        # now that all neighbors have been visited: recurse                         
        # select the non visited node with lowest distance 'x'
        # run Dijskstra with src='x'
        unvisited={}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))        
        x=min(unvisited, key=unvisited.get)
        dijkstra(graph,x,dest,visited,distances,predecessors)
        #return path

def cal_flows(switch, graph,path):
    print "In fucntion"
    #print len(path)
    for i in range (0,len(path)):
        if i !=len(path)-1:
            next1=path[i+1]
            cur =path[i]
            if i != 0:
                prev = path[i-1]
            last=path[len(path)-1]
            next_dict=graph[next1]
            current_dict=graph[cur]
            #print last
            if cur in switch:
                dpid= switch[cur]
            if(cur in graph.keys()):
                if(next1 in current_dict.keys()):
                    outgoing = current_dict[next1]
                    if (next1 in graph.keys()):
                        if cur in next_dict.keys() and i != 0:
                            incoming=current_dict[prev]
                    if i==0:
                        print "Switch "+ str(dpid) +" Outgoing "+ str(outgoing) #" incoming " + str(incoming)
                        if dpid == "00:00:00:00:00:00:00:03" or dpid == "00:00:00:00:00:00:00:04":
                        	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"' + str(dpid) + '", "name":"h40s4' + str(i) + '", "priority":"123", "in_port" : "'+ str(1) +'","actions":"output='+ str(outgoing) +'"}')
                    		requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"' + str(dpid) + '", "name":"h40s4' + str(i + 100) + '", "priority":"123", "in_port" : "'+ str(2) +'","actions":"output='+ str(outgoing) +'"}')
                        # print "switch :" + dpid +  ",name":"h40s42," "priority":"1, in_port : "+ incoming +" ,actions: output=" + 'outgoing                       

                    else:
                    	flow_name = str(cur) + str(outgoing) + str(next1) + str(incoming)
                    	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"' + str(dpid) + '", "name":"h40s4' + str(i) + '", "priority":"123", "in_port" : "'+ str(incoming) +'","actions":"output='+ str(outgoing) +'"}')
                    	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"' + str(dpid) + '", "name":"h40s4' + str(i + 100) + '", "priority":"123", "in_port" : "'+ str(outgoing) +'","actions":"output='+ str(incoming) +'"}')
                    	# x = '{"switch":"' + str(dpid) + '", "name":"h40s4' + str(i) + '", "priority":"123", "in_port" : "'+ str(incoming) +'","actions":"output='+ str(outgoing) + '"}'
                    	# 
                        print x
                    	# requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":' + str(dpid) + ', "name":"h40s4"' + str(i) + ', "priority":"1", "in_port" : '+ str(outgoing) +',"actions":"output=" '+ str(incoming) +'}')
                        # print '{"switch":' + str(dpid) + ', "name":"h40s4"' + str(i) + ', "priority":"1", "in_port" : '+ str(incoming) +',"actions":"output=" '+ str(outgoing) +'}'
                        print "Switch "+ str(dpid) +" Outgoing "+ str(outgoing)+ " incoming " + str(incoming)
                        print "Switch "+ str(dpid) +" Outgoing "+ str(incoming)+ " incoming " + str(outgoing)
        else:
            cur = path[i]
            prev = path[i-1]
            current_dict = graph[cur]
            prev_dict = graph[prev]
            incoming = current_dict[prev]
            outgoing = incoming
            dpid = switch[cur]
            print "Switch "+ str(dpid) +" Outgoing "+ str(outgoing)#+ " incoming " + str(incoming)
            print "Switch "+ str(dpid) + "incoming " + str(incoming)


graph = {'s1': {'s2': 1, 's3': 10, 's4': 1},
            's2': {'s1':1 , 's3': 1, 's4':1},
            's3': {'s2': 1, 's4': 10, 's1': 10},
            's4': {'s1': 1, 's2': 1, 's3': 1}}
graph1={'s1': {'s2': 5, 's3': 3, 's4': 4},
        's2': {'s1':5 , 's3': 3, 's4':4},
        's3': {'s2': 4, 's4': 5, 's1': 3},
        's4': {'s1': 3, 's2': 5, 's3': 4}}
switch = {'s1': "00:00:00:00:00:00:00:01",
        's2': "00:00:00:00:00:00:00:02",
        's3': "00:00:00:00:00:00:00:03",
        's4': "00:00:00:00:00:00:00:04"}




def stats_collector():
	i = 0
	# time.sleep(10)
	while i < 10:
		os.system("tc -s -d -p qdisc show dev s3-eth1 >> output.txt")
		i += 1
		time.sleep(5)


def func():
	i = 0
	time.sleep(3)
	prev = [0,0,0]
	cur = [0,0,0]
	diff = [0,0,0]
    	flag = 0
	while(i < 1000):
    		bw_stats=requests.get(url= "http://127.0.0.1:8080/wm/core/switch/00:00:00:00:00:00:00:03/port/json")
    		bw_json=json.loads(bw_stats.text)
    		for port in bw_json['port_reply'][0]['port']:
    			if port['port_number'] != 'local' and int(port['port_number']) in range(3,6):
    				cur[int(port['port_number']) - 3] = int(port['transmit_bytes']) + int(port['receive_bytes'])
    			# f.write("Port Num: " + port['port_number'] + " \tTransmit bytes: " + port['transmit_bytes'] + " \tReceive bytes: " + port['receive_bytes'] + " \tTransmit Dropped: " + port['transmit_dropped'] + " \tReceive dropped: " + port['receive_dropped'] + '\n')
    		# f.write(str(bw_json))
    		for i in range(0,len(cur)):
    			# f.write(" Cur: " + str(cur[i]) + " Prev: " + str(prev[i]))
    			diff[i] = cur[i] - prev[i]
    			f.write(" Cur: " + str(cur[i]) + " Prev: " + str(prev[i]) + " Bandwidth: " + str((diff[i] * 8)/(5)) + "\n")
    			# f.write("Diff for port " + str(i+3) + "is " + str(diff[i]) + "\n")
    		if (diff[0] * 8)/5 > 3500000:
    			f.write("CONGESTEDDDDDD\n")
                	if flag == 0:
            			os.system("curl http://0.0.0.0:8080/wm/staticentrypusher/clear/all/json")
                	    	flag = 1 
    				flows()
    		f.write("\n\n")
    		i += 1
		# print arr
		for i in range(0,len(cur)):
			prev[i] = cur[i]
    		time.sleep(5)
    	# print arr    

def flows():
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"af9", "priority":"1", "eth_dst": "00:00:00:00:00:01","actions":"output=1"}')
 
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"af10", "priority":"1", "eth_dst": "00:00:00:00:00:02","actions":"output=2"}')

	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"af12", "priority":"1", "in_port" : "5","actions":"output=1"}')

	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"af11", "priority":"1", "in_port" : "3","actions":"output=5"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"af13", "priority":"1", "in_port" : "5","actions":"output=3"}')
	
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"af14", "priority":"1", "eth_dst": "00:00:00:00:00:02","actions":"output=4"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"af15", "priority":"1", "eth_dst": "00:00:00:00:00:01","actions":"output=3"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"af1", "priority":"1", "eth_src": "00:00:00:00:00:01","actions":"output=3"}')
	
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:03", "name":"af2", "priority":"1", "eth_src": "00:00:00:00:00:02","actions":"output=4"}') 
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"af3", "priority":"1", "in_port": "3","actions":"output=1"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"af4", "priority":"1", "in_port": "1","actions":"output=4"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"af5", "priority":"1", "in_port": "5","actions":"output=2"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"af20", "priority":"1", "in_port": "3","actions":"output=4"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:04", "name":"af6", "priority":"1", "in_port": "2","actions":"output=5"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:02", "name":"af7", "priority":"1", "in_port": "4","actions":"output=1"}')
	requests.post(url='http://127.0.0.1:8080/wm/staticentrypusher/json', data='{"switch":"00:00:00:00:00:00:00:01", "name":"af8", "priority":"1", "in_port": "1","actions":"output=3"}')


# flag = 0
f = open("output.txt", "a")
# f = open("output1.txt", "a")
arr = []
topos = { 'mytopo': ( lambda:MyTopo() )}
# thread = Thread(target=func())
# thread.start()
# thread.start_new_thread(stats_collector,())
#thread.start_new_thread(func,())
