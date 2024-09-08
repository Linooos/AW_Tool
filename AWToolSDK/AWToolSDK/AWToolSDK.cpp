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
#endif // ALIEN_FAN_SDK

int32_t testfct()
{
    return 42;
}
