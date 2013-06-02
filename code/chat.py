# -*- coding: utf-8 -*-
"""
Created on Sat Jun 01 20:28:49 2013

@author: wy
"""

import sys
import socket
import SocketServer
import threading
import cPickle


class chatServer(SocketServer.ThreadingTCPServer):
    '''
    服务器程序。
    '''
    def __init__(self, server_address, RequestHandlerClass, mainserver=False,bind_and_activate=True):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)
        self.allclients={}
        self.mainserver = mainserver
        print 'Listent at',server_address,mainserver


class myHandler(SocketServer.BaseRequestHandler):
    '''
    请求处理，响应每一次连接请求。
    '''
    def handle(self):
        data2 = self.request.recv(1024)
        data = cPickle.loads(data2)
        clients=[client[0] for client in self.server.allclients]
        print data['name'],u' 说: ',data['say']
        #print 'mainserver',self.server.mainserver
        #以下是主机的部分：
        if self.server.mainserver:
            #if not data['name'] in clients:
            self.server.allclients[data['name']]=self.client_address[0]
            msg = data2
            for o in self.server.allclients:
                #print o
                if self.server.allclients[o]!=self.server.server_address:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:                
                        sock.connect((self.server.allclients[o],8887))
                        sock.sendall(msg)
                    except:
                        pass
                    finally:
                        sock.close()
        
        
        
class client():
    '''
    客户端。
    '''
    def __init__(self,name,host='localhost',port=8888):
        self.name = name
        self.host = host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.connect(self.host,self.port)            
    def say(self):
        '''
        发出消息。
        '''        
        while 1:
            i = raw_input(self.name+'>>')
            data = {'name':self.name,'say':i}
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host,self.port))
                self.sock.sendall(cPickle.dumps(data))
            except:
                print 'error'
            finally:
                self.sock.close()
            
def main(name,targetaddr,mainserver=False):
    '''    
    主程序.
    '''
    if mainserver:
        selfserver=chatServer(('0.0.0.0',8888),myHandler,mainserver)
    else:
        selfserver=chatServer(('0.0.0.0',8887),myHandler,mainserver)
    sthread = threading.Thread(target=selfserver.serve_forever)
    sthread.daemon = True
    sthread.start()
    selfclient=client(name,targetaddr)
    selfclient.say()
        
if __name__=='__main__':
    if len(sys.argv)==3:
        name = sys.argv[1]
        targetaddr = sys.argv[2]
        print targetaddr,False
        main(name,targetaddr)
    elif len(sys.argv)>3:
        name = sys.argv[1]
        targetaddr = sys.argv[2]
        t = int(sys.argv[3])
        print targetaddr,t
        main(name,targetaddr,t)
    else:
        import os
        # print u'请在命令行模式启动并添加参数： 客户端名 目标地址 [主机]'
        # print u'例如：'
        # print u'./server3 name 0.0.0.0'
        print u'请输入你想使用的姓名'
        name = raw_input()
        print u"请输入目标地址，主机请用127.0.0.1"
        targetaddr = raw_input()
        print u'是否主机（1/0）'
        t = input()
        main(name,targetaddr,t)
        os.system('pause')
                
        
            
