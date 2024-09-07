// AWToolSDK.cpp : 定义 DLL 的导出函数。
//
#include "pch.h"
#include "framework.h"
#include "AWToolSDK.h"

// 这是导出变量的一个示例
AWTOOLSDK_API int nAWToolSDK=0;

// 这是导出函数的一个示例。

// 这是已导出类的构造函数。
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

FanControl* pCtrlr = new FanControl();
