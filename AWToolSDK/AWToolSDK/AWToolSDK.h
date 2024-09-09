#pragma once

#define ALIEN_FAN_SDK
#ifdef ALIEN_FAN_SDK //SDK中添加风扇控制函数
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
    LONG checkAPI(byte type);

	//get
	
	AlienFan_SDK::ALIENFAN_SEN_INFO* getSensor(DWORD index);

	//Fan

	/// <summary>
	/// 获取风扇的id和type
	/// </summary>
	/// <param name="index">index</param>
	/// <returns>return->id,return->type</returns>
	LONG getFan(DWORD index, AlienFan_SDK::ALIENFAN_FAN_INFO& info);
	/// <summary>
	/// 返回指定风扇的最大转速
	/// </summary>
	/// <param name="fanid">风扇id</param>
	/// <returns>转速</returns>
	LONG getMAXFan(BYTE index);
	/// <summary>
	/// 返回风扇总数，以风扇数量作为index用getFan函数获取风扇id和风扇类别
	/// </summary>
	/// <returns>总数,减一为index</returns>
	DWORD getFansCount();
	/// <summary>
	/// 获取指定风扇的当前转速
	/// </summary>
	/// <param name="fanid">由getFan()->id获取</param>
	/// <returns>转速</returns>
	LONG getFanRPM(BYTE index);
	/// <summary>
	/// 解锁自行控制风扇
	/// </summary>
	/// <returns>-1：错误，0：成功</returns>
	LONG unlockFanControl();
	
	//Power

	/// <summary>
	/// 获取当前电源模式
	/// </summary>
	/// <param name="index"></param>
	/// <returns></returns>
	//BYTE getPower(DWORD index);
	//BYTE getPowersCount(DWORD index);
	//BYTE getCurPower(DWORD index);


	//set
	
	//Fan
	
	/// <summary>
	/// 设置风扇转速
	/// </summary>
	/// <param name="fanid">风扇id</param>
	/// <param name="value">转速的映射值，0-255范围</param>
	/// <returns></returns>
	DWORD setFan(BYTE index, BYTE value);



	
	// TODO: 在此处添加方法。
};
#endif //ALIEN_FAN_SDK

int32_t testfct();
//AWTOOLSDK_API int fnAWToolSDK(void);
