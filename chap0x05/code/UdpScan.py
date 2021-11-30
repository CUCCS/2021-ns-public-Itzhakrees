from scapy.all import *


def UdpScan(dstip,dstport,srsport):
    pkt = IP(dst=dstip)/UDP(dport=int(dstport),sport=srsport)
    ans = sr1(pkt,timeout=1,verbose=0)
    
    if ans is None:
        print(dstip,' port:',dstport,'is open or filtered.')
    elif ans.haslayer(UDP):
        print(dstip,' port:',dstport,'is open.')
    elif ans.haslayer(ICMP):
        if int(ans.getlayer(ICMP).type)==3 and int(ans.getlayer(ICMP).code)==3:
            print(dstip,' port:',dstport,'is closed')

if __name__=='__main__':
    dst_ip="172.16.111.115"
    dst_port="8080"
    srs_port=RandShort() #必须要一个源端口号，否则包会因为不符合要求而被丢弃，就不知道目标端口会不会发送包
    
    print("acitvating UDP scan......\n")
    UdpScan(dst_ip,dst_port,srs_port)
    print("\nscan has compeleted.")
