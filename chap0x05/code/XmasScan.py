#!/usr/bin/env python3

from scapy.all import *

def XmasScan(dstip,dstport):
    pkt=IP(dst=dstip)/TCP(dport=dstport,flags="FPU")
    ans = sr1(pkt,timeout=1,verbose=0)
    if ans is None:
        print(dstip,' port:',dstport,'is open or filtered.')
    elif(ans.haslayer(TCP)):
        if(ans[1].flags == "RA"):
            print(dstip,' port:',dstport,'is closed')
    

if __name__=='__main__':
    dst_ip="172.16.111.115"
    dst_port=8080

    print("acitvating TCP-Xmas scan......\n") #真的很想写成Xmax(因为有辆喜欢的摩托车叫XMAX)
    XmasScan(dst_ip,dst_port)
    print("\nscan has compeleted.")