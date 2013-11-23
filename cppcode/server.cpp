
#include "socket_head.h"



int main()
{

	int mainserver;
	WORD sockVersion = MAKEWORD(2,2);  
    WSADATA wsaData;  
    if(WSAStartup(sockVersion, &wsaData)!=0)  
    {  
        return 0;  
    }  
	cout<<"mainserver?"<<endl;
	cin>>mainserver;

	TcpServer server = TcpServer(bool(mainserver));
	server.runserver();


}