#include "iostream"
#include "winsock.h"
#include "windows.h"
#include "stdlib.h"
#include "string"
//#include "set"
//#include "vector"
//#include <process.h>
#pragma comment(lib,"ws2_32.lib")  
//#pragma warning(disable:4996)


using namespace std;



class TcpServer
{
	SOCKET listenSock;
	SOCKADDR_IN listenAddr;
	bool mainserver;
	SOCKET acceptSock;
	SOCKADDR_IN acceptAddr;
	int acceptLen;
	char recvData[5000];
	bool printing;
public:
	TcpServer(bool mainserver)
	{
		listenSock = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
		listenAddr.sin_family = AF_INET;
		listenAddr.sin_addr.S_un.S_addr = INADDR_ANY;
		listenAddr.sin_port = htons((mainserver)?8888:8887);
		if(bind(listenSock,(sockaddr*)&listenAddr,sizeof(listenAddr)) == -1)
		{
			cout<<"bind error."<<endl;
		}
		if(listen(listenSock,10) == -1)
		{
			cout<<"listen failed."<<endl;
		}



		acceptLen = sizeof(acceptAddr);
		printing = false;
		//system("PAUSE");
	}
	void handler()
	{
		acceptSock = accept(listenSock,(sockaddr*)&acceptAddr,&acceptLen);
		if(acceptSock == INVALID_SOCKET)
		{
			cout<<"accept error"<<endl;
			return;
		}
		int recLen = recv(acceptSock,recvData,5000,0);
		if(recLen>0)
		{
			recvData[recLen] = '\0';
			while(printing)
				continue;
			printing = true;
			cout<<recvData<<endl;
			printing = false;
		}
		closesocket(acceptSock);


	}
	void runserver()
	{
		while(true)
		{
			handler();
		}
	}
};

class TcpClient
{
	SOCKET client;
	SOCKADDR_IN serAddr;

public:
	TcpClient(string serAddrIP)
	{
		client = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		serAddr.sin_family = AF_INET;
		serAddr.sin_addr.S_un.S_addr = inet_addr(serAddrIP.c_str());
		serAddr.sin_port = htons(8888);

	}
	void senddata(string data)
	{
		client = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
		if (connect(client, (sockaddr *)&serAddr, sizeof(serAddr)) == SOCKET_ERROR)  
		{  
			cout<<"connect error !"<<endl;  
			closesocket(client);  
			return;  
		}  
		send(client,data.c_str(),data.length(),0);
		closesocket(client);

	}
};




