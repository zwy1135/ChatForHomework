# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:09:34 2013

@author: wy
"""

import sys
import socket
import SocketServer
import threading
import pickle


class Udp(SocketServer.ThreadingUDPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        SocketServer.ThreadingUDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        self.printing = 0
        #print "启动成功。"


class udphandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        data2 = pickle.loads(data)
        while self.server.printing:
            pass
        self.server.printing = 1
        print data2['name'],u'说：',data2['words']
        self.server.printing = 0
        
class client:
    def __init__(self,name,target,success,port = 4892):
        self.name = name
        self.target = target
        self.port = int(port)
        self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if success:        
            print u'启动成功。'        
        else:
            print u'启动失败。'
    def send(self):
        while 1:
            i = raw_input()
            data = {'name':self.name,'words':i}
            try:
                self.so.sendto(pickle.dumps(data),(self.target,self.port))
            except:
                print u'error:刚才的话没发出去。'
                
def main():
    print u'请输入你想要用的名字：'
    name = raw_input()
    print u'请输入对方ip。'
    target = raw_input()
    print u'启动中。'
    su = 1    
    try:
        ser = Udp(('0.0.0.0',4892),udphandler)
    except:
        print u'本机已有一个相同程序在运行。'
        su = 0
        ser = Udp(('0.0.0.0',4891),udphandler)
    sth = threading.Thread(target = ser.serve_forever)
    sth.daemon = True
    sth.start()
    c = client(name,target,su)
    c.send()
    
if __name__=='__main__':
    main()
    
        
        