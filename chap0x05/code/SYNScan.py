#!/usr/bin/env python3

from scapy.all import *


def Synscan(ip,port):
    dstip=IP(dst=ip)/TCP(dport=int(port),flags="S")
    ans=sr1(dstip,timeout=1,verbose=0)
  
    if ans is None:
        print(ip,' port:',port,'is filtered.')
    elif ans.haslayer(TCP):
        if ans[1].flags=='SA':
            resend_ans=sr1(IP(dst=ip)/TCP(dport=port,flags="R"),timeout=1,verbose=0)
            print(ip,' port:',port,'is open.')
        else:
            print(ip,' port:',port,'is closed.')

if __name__=='__main__':
    ip="172.16.111.115"
    port=8080
    print("acitvating TCP-SYN scan......\n")
    Synscan(ip,port)

    print("scan has compeleted.\n")
