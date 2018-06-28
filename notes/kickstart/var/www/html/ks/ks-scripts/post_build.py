#!/usr/bin/python
HOST_DEF = []
import os
import platform

def define_host():
	os.system('clear')
	print "\n\n"
        HOST_DEF.append(raw_input ("What is your hostname: "))
        HOST_DEF.append(raw_input ("What is your domain: "))
        HOST_DEF.append(raw_input ("What is your IP address: "))
        HOST_DEF.append(raw_input ("What is your netmask: "))
        HOST_DEF.append(raw_input ("What is your default gateway: "))
        print "Which interface will your server be using: "
        CNT=1
        INTERFACES = {}

	""" For all lines in /proc/net/dev, to obtain all available interfaces """
        NET_FILE = open('/proc/net/dev', 'r')
        for LINE in NET_FILE:
                if "lo:" not in LINE:
                        if "Inter" not in LINE:
                                if "face" not in LINE:
                                        INTERFACES[CNT] = LINE.split(":")[0] 
                                        print "%d ) %s" % (CNT, INTERFACES[CNT])
                                        CNT += 1
        NET_FILE.close()

        DEVICE = int(raw_input ("Select the number: "))
        HOST_DEF.append(INTERFACES[DEVICE].lstrip())
	
	print "What type of environment are you building:"
	ENVIRONMENTS = [ 'lab', 'infrastructure', 'oracle-prod', 'oracle-web', 'oracle-non-prod', 'web', 'other-prod', 'other-non-prod']
	for ENV_CNT in range(0, len(ENVIRONMENTS)):
		print "%d ) %s" % (ENV_CNT + 1, ENVIRONMENTS[ENV_CNT])

	HOST_ENV = int(raw_input ("Select the number: ")) - 1
	HOST_DEF.append(ENVIRONMENTS[HOST_ENV].lstrip())

        print "\n"

	""" Confirmation of information provided """
        print "This is this information you provided: "
        print "Hostname        = %s" % HOST_DEF[0]
        print "Domain          = %s" % HOST_DEF[1]
        print "IP Address      = %s" % HOST_DEF[2]
        print "Netmask         = %s" % HOST_DEF[3]
        print "Default Gateway = %s" % HOST_DEF[4]
        print "Interface       = %s" % HOST_DEF[5]
	print "Environment     = %s" % HOST_DEF[6]

	""" Obtaing MAC Address and populate field 8 in HOST_DEF """
        NET_MAC_FILE = open ('/sys/class/net/%s/address' % HOST_DEF[5])
        for NET_MAC_LINE in NET_MAC_FILE:
                HOST_DEF.append(NET_MAC_LINE.rstrip('\n'))
        NET_MAC_FILE.close()

        ANS2 = raw_input ("Is this correct [y/n]: ")
        if ANS2 == 'y' or ANS2 == 'Y':
                return HOST_DEF
        else:
                del HOST_DEF[:]
                define_host()

""" RHEL 7 /etc/hostname file """
def write_hostname7(HOST_LIST):
	HOSTNAME_FILE = open ('/etc/hostname', 'w')
	HOSTNAME_FILE.write(HOST_LIST[0] + '.' + HOST_LIST[1] + '\n')
	HOSTNAME_FILE.close()

def write_ifcfg(HOST_LIST):
        IFCFG_FILE = open ('/etc/sysconfig/network-scripts/ifcfg-%s' % HOST_LIST[5], 'w')
        IFCFG_FILE.write("DEVICE=" + HOST_LIST[5] + '\n');
        IFCFG_FILE.write("BOOTPROTO=static" + '\n');
        IFCFG_FILE.write("IPADDR=" + HOST_LIST[2] + '\n');
        IFCFG_FILE.write("NETMASK=" + HOST_LIST[3] + '\n');
        IFCFG_FILE.write("HWADDR=" + HOST_LIST[7] + '\n');
        IFCFG_FILE.write("ONBOOT=yes" + '\n');
        IFCFG_FILE.close()

""" RHEL 7 /etc/sysconfig/network file """
def write_network7(HOST_LIST):
	NETWORK_FILE = open ('/etc/sysconfig/network', 'w')
        NETWORK_FILE.write("NETWORKING=yes" + '\n')
        NETWORK_FILE.write("GATEWAY=" + HOST_LIST[4] + '\n')
        NETWORK_FILE.close()

""" RHEL 4,5,6 /etc/sysconfig/network file """
def write_network(HOST_LIST):
	NETWORK_FILE = open ('/etc/sysconfig/network', 'w')
        NETWORK_FILE.write("NETWORKING=yes" + '\n')
        NETWORK_FILE.write("HOSTNAME=" + HOST_LIST[0] + '.' + HOST_LIST[1] + '\n')
        NETWORK_FILE.write("GATEWAY=" + HOST_LIST[4] + '\n')
        NETWORK_FILE.close()

def write_hosts(HOST_LIST):
        HOSTS_FILE = open ('/etc/hosts', 'a')
        HOSTS_FILE.write(HOST_LIST[2] + '\t' + HOST_LIST[0] + '\t' + HOST_LIST[0] + "." + HOST_LIST[1] + '\n')
        HOSTS_FILE.close()

def write_resolv():
        RESOLV_FILE = open ('/etc/resolv.conf', 'w')
        RESOLV_FILE.write("search starkey.com ms.starkey.com" + '\n')
        RESOLV_FILE.write("nameserver 10.40.0.222" + '\n')
        RESOLV_FILE.write("nameserver 10.129.64.222" + '\n')
        RESOLV_FILE.close()

def update_fstab():
	FSTAB_FILE = open ('/etc/fstab', 'a')
	FSTAB_FILE.write('nfs.starkey.com:/ifs/nfs/unix' + '\t' + '/opt/depots' + '\t' + 'nfs' + '\t' + 'soft,rw' + '\t' + '0 0\n')
	FSTAB_FILE.close()

def write_env(HOST_LIST):
	ENV_FILE = open ('/etc/puppet.environ', 'w')
	ENV_FILE.write(HOST_LIST[6] + '\n')
	ENV_FILE.close()

define_host()

OS_VER = platform.linux_distribution()[1].split(".", 1)[0]

if OS_VER == '7':
	write_hostname7(HOST_DEF)
	write_network7(HOST_DEF)
else:
	write_network(HOST_DEF)

write_ifcfg(HOST_DEF)
write_hosts(HOST_DEF)
write_resolv()
update_fstab()
write_env(HOST_DEF)