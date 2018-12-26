# Congestion-control-in-software-defined-data-center-networks
Developed a congestion control algorithm by making the SDN controller continually analyze congested links and rerouting selected traffic to less congested links.

The following steps have to be implemented before running the python file.

1) sudo apt-get install build-essential ant maven python-dev

The following instructions are for installing Floodlight from Scratch

1) git clone git://github.com/floodlight/floodlight.git
2) cd floodlight
3) git submodule init
4) git submodule update
5) ant
6) sudo mkdir /var/lib/floodlight
7) sudo chmod 777 /var/lib/floodlight

Updating an Existing Floodlight Installation:

1) cd floodlight
2) git pull origin master
3) git submodule init
4) git submodule update

Installing mininet on ubuntu:
1) git clone git://github.com/mininet/mininet
2) cd mininet
3) git tag 			#lists available versions
4) git checkout -b 2.2.1 2.2.1    #or any version that the user wants to install
5) cd ..

Once you have the source tree, the command to install Mininet is:
1) mininet/util/install.sh -a  # -a is an option to install all packages of mininet

Install base mininet package with the following command:
1) sudo apt-get install mininet

If Mininet complains that Open vSwitch isn’t working, you may need to rebuild its kernel module:
1) sudo dpkg-reconfigure openvswitch-datapath-dkms
2) sudo service openflow-switch restart

Once the setup is complete navigate to the floodlight folder:
1) cd floodlight 
2) java -jar target/floodlight.jar
Open another terminal and navigate to the floodlight folder.
3) sudo mn --custom [[name of python file]] --topo=[[name of topology]] --mac --switch ovsk --controller=remote,ip=<controller-ip>,port=6653 --link=tc
4) Once the mininet CLI opens, type the following command:
a) xterm h1 h2 h4 						#to perform the iperf test
The above command will open 3 more command windows, with the names of the hosts on top.
For host h4 (server) : iperf -s -u                 #acts as server
For host h1 and h2: iperf -c 10.0.3.20 -b 4M -t 30

Observe the packet losses and bandwidth in the cmd.

Other helpful commands: dpctl dump-flows (for checking flows added to the controller)
						ping (for pinging between source and destination)
						traceroute
						<switch> route  (for checking routes of a particular switch)

