from  threading import Thread
from queue import Queue
import  sys
import re
import socket
IpConPA=[]
class ScanPortc(Thread):    
    def __init__(self, target_ip, target_port, q,ipx):
        super(ScanPortc, self).__init__()
        self.target_ip = target_ip
        self.target_port = target_port
        self.q = q
        self.ipx=ipx

    def scan_port(self):
        try:               
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
            s.connect((self.target_ip, self.target_port))            
            q.put(str(self.target_port) + ' is opening')            
            self.ipx.append([self.target_ip,self.target_port])          
            s.close()          
        except Exception :              
            pass

    def run(self):
       self.scan_port()

q = Queue()

def Scan(ip,port):
    x,x1=ScanPort(ip,port)     
    return x,x1

def ScanPort(ip,port_list):         
    portThreadList = [ ScanPortc(ip, port, q,IpConPA) for port in port_list ]
    #portThreadList = [ ScanPort(ip, port, q) for port in range(0,65000) ]
    for t in portThreadList:
        t.setDaemon(True)
        t.start()

    for t in portThreadList:
        t.join()

    # END enters the queue, indicating the end of the scan
    q.put('end')    
    while True:      
        result = q.get()            
        if re.search(r'end', result):   
            break
    return q,IpConPA