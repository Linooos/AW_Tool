#pragma once

#define ALIEN_FAN_SDK
#ifdef ALIEN_FAN_SDK
#include "alienfan-SDK.h"
//#include <string>

//api的判断类型
enum{
	isAlienware = 0,
	isSupported= 1,
	isTCC = 2,
	isXMP = 3,
	isGmode = 4
};

class FanControl {
public:
	FanControl();
	~FanControl();
	AlienFan_SDK::Control* controller;
	BOOL isAPIValid;
	CHAR checkAPI(byte type);

	//get

	////读取初始化时检测的sensors列表并返回index代表的传感器属性
	////return：nullptr错误（参数）
	//AlienFan_SDK::ALIENFAN_SEN_INFO* getSensor(DWORD index);
	////读取初始化时检测的fans列表并返回index代表的风扇属性
	////return：nullptr错误（参数）
	//AlienFan_SDK::ALIENFAN_FAN_INFO* getFan(DWORD index);
	//BYTE getPower(DWORD index);
	//DWORD getFanRPM(BYTE fanid);
	//DWORD getMaxRPM(BYTE fanid);

	////set
	//DWORD unlockFanControl();
	//DWORD setFan(BYTE fanid, BYTE value);


	
	// TODO: 在此处添加方法。
};
#endif

int32_t testfct();
//AWTOOLSDK_API int fnAWToolSDK(void);
