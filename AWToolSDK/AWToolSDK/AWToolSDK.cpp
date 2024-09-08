// AWToolSDK.cpp : 定义 DLL 的导出函数。
//
#include <pybind11/pybind11.h>
#include "AWToolSDK.h"

#ifdef ALIEN_FAN_SDK
FanControl::FanControl()
{
    this->controller = new AlienFan_SDK::Control();
    this->isAPIValid = this->controller->Probe();
}

FanControl::~FanControl()
{
    this->controller->~Control();
}

CHAR FanControl::checkAPI(byte type)
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
