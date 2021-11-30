#!/usr/bin/env python3

from scapy.all import *


def TCP_Connection(ip,port):
    
    pkt=IP(dst=ip)/TCP(dport=int(port))

    ans=sr1(pkt,timeout=1,verbose=0)

    if ans is None:
        print(ip,' port:',port,'is filtered.')
    elif (ans.haslayer(TCP)):
        if ans[1].flags=='SA':
            print(ip,' port:',port,'is open.')
        elif ans[1].flags=='RA':
            print(ip,' port:',port,'is closed.')

if __name__=='__main__':
    ip="172.16.111.115"
    port="8080"
    print("acitvating TCP-Connection scan......\n")
    TCP_Connection(ip,port)

    print("\nscan has compeleted.\n")
