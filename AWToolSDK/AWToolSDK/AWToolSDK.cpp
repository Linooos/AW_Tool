// AWToolSDK.cpp : 定义 DLL 的导出函数。
//
#include <pybind11/pybind11.h>
#include "AWToolSDK.h"

#ifdef ALIEN_FAN_SDK
FanControl::FanControl()
{
    this->controller = new AlienFan_SDK::Control();
#ifdef _DEBUG
    printf("Run controller probe!\n");
#endif // 
    this->isAPIValid = this->controller->Probe();
#ifdef _DEBUG
    printf("SDK initialize complete!\n");
#endif // 
}

FanControl::~FanControl()
{
    this->controller->~Control();
}

LONG FanControl::checkAPI(byte type)
{
    if (type == isAlienware)
        return this->controller->isAlienware;
    if (type == isSupported)
        return this->controller->isSupported;
    if (type == isTCC)
        return this->controller->isTcc;
    if (type == isXMP)
        return this->controller->isXMP;
    if (type == isGmode)
        return this->controller->isGmode;

    return -1;
}

AlienFan_SDK::ALIENFAN_SEN_INFO* FanControl::getSensor(DWORD index)
{
    return nullptr;
}
LONG FanControl::getFan(DWORD index,AlienFan_SDK::ALIENFAN_FAN_INFO &info)
{
    //检查参数   
    if (index >= (this->getFansCount())) {
#ifdef _DEBUG
        printf("Error index\n");
#endif // _DEBUG
        return -1;
    }
#ifdef _DEBUG
    printf("Get fan info:%d\n",index);
#endif // _DEBUG
    info = this->controller->fans.at(index);
    return 0;
}
LONG FanControl::getMAXFan(BYTE index)
{
    return this->controller->GetMaxRPM(index);
}
DWORD FanControl::getFansCount()
{
    return (DWORD)this->controller->fans.size();
}
LONG FanControl::getFanRPM(BYTE index)
{
    return this->controller->GetFanRPM(index);
}
LONG FanControl::unlockFanControl()
{
    return this->controller->Unlock();
}
DWORD FanControl::setFan(BYTE index, BYTE value)
{
    return this->controller->SetFanBoost(index,value);
}
#endif // ALIEN_FAN_SDK

int32_t testfct()
{
    return 42;
}
