// 下列 ifdef 块是创建使从 DLL 导出更简单的
// 宏的标准方法。此 DLL 中的所有文件都是用命令行上定义的 AWTOOLSDK_EXPORTS
// 符号编译的。在使用此 DLL 的
// 任何项目上不应定义此符号。这样，源文件中包含此文件的任何其他项目都会将
// AWTOOLSDK_API 函数视为是从 DLL 导入的，而此 DLL 则将用此宏定义的
// 符号视为是被导出的。
#pragma once

#ifdef AWTOOLSDK_EXPORTS
#define AWTOOLSDK_API __declspec(dllexport)
#else
#define AWTOOLSDK_API __declspec(dllimport)
#endif



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

extern AWTOOLSDK_API FanControl* pCtrlr;

//AWTOOLSDK_API int fnAWToolSDK(void);
