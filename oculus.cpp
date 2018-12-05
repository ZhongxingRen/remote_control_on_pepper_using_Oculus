#include <WINSOCK2.H>
#include <stdio.h>
#include<sstream>
//定义程序中使用的常量
#define SERVER_ADDRESS "127.0.0.1"
#define PORT 12345//服务器的端口号
#define MSGSIZE 1024//收发缓冲区的大小
#pragma comment(lib, "ws2_32.lib")

#include <iostream>
#include <iomanip>
#include <OVR_CAPI.h>
#include <thread>

#define COLW setw(15)

using namespace std;

int main()
{   // Initialize our session with the Oculus HMD.



	WSADATA wsaData;
	SOCKET sClient;
	SOCKADDR_IN server;
	char szMessage[MSGSIZE];
	int ret;
	WSAStartup(0x0202, &wsaData);
	sClient = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	memset(&server, 0, sizeof(SOCKADDR_IN));
	server.sin_family = PF_INET;
	server.sin_port = htons(PORT);
	server.sin_addr.s_addr = inet_addr(SERVER_ADDRESS);
	connect(sClient, (struct sockaddr *) &server, sizeof(SOCKADDR_IN));






	if (ovr_Initialize(nullptr) == ovrSuccess)
	{
		ovrSession session = nullptr;
		ovrGraphicsLuid luid;
		ovrResult result = ovr_Create(&session, &luid);

		if (result == ovrSuccess)
		{   // Then we're connected to an HMD!

			// Let's take a look at some orientation data.
			ovrTrackingState ts;
			while (true)
			{
				ts = ovr_GetTrackingState(session, 0, true);

				ovrPoseStatef tempHeadPose = ts.HeadPose;
				ovrPosef tempPose = tempHeadPose.ThePose;
				ovrQuatf tempOrient = tempPose.Orientation;
				string strx=to_string(tempOrient.x);
				string stry= to_string(tempOrient.y);
				string strsend = strx + "," + stry;
				strcpy(szMessage, strsend.c_str());//strsend内容送到字符数组中。
				//cout << "Orientation (x,y,z):  " << COLW << tempOrient.x << ","
					//<< COLW << tempOrient.y << "," << COLW << tempOrient.z
					//<< endl;

				send(sClient, szMessage, strlen(szMessage), 0);
				// Wait a bit to let us actually read stuff.

				std::this_thread::sleep_for(std::chrono::milliseconds(800));
			}

			ovr_Destroy(session);
		}

		ovr_Shutdown();
		// If we've fallen through to this point, the HMD is no longer
		// connected.
	}
	closesocket(sClient);
	WSACleanup();
	return 0;
}