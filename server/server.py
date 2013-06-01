# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:48:33 2013

@author: wy
"""

import sys
import socket
import threading
import SocketServer


class MyHandler(SocketServer.BaseRequestHandler):
    '''
    请求处理部分    
    '''
    def handle(self):
        data = self.request.recv(1024)
        #cur_th = threading.current_thread()
        response = data
        self.request.sendall(response)
        
class MyTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    '''
    服务器主体，继承了现有类所以完全不需修改。
    '''
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

def main(HOST='localhost',PORT=8888):
    '''
    
    '''
    server = MyTCPServer((HOST,PORT),MyHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    ip, port = server.server_address
    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")
    
if __name__=='__main__':
    if sys.argv[1:]:
        print 'Run at ',sys.argv[1:]
        main(sys.argv[1],int(sys.argv[2]))
    else:
        main()
    print 'All normal.'