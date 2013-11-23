#include "socket_head.h"

int main()
{
	WORD sockVersion = MAKEWORD(2,2);  
    WSADATA wsaData;  
    if(WSAStartup(sockVersion, &wsaData)!=0)  
    {  
        return 0;  
    }  
	string serIP;
	cout<<"Input server IP."<<endl;
	getline(cin,serIP);
	TcpClient client = TcpClient(serIP);
	while(true)
	{
		client.senddata(serIP);
		Sleep(2000);
	}
}