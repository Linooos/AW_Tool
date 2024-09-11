// AWToolSDK.cpp : 定义 DLL 的导出函数。
//
#include <pybind11/pybind11.h>
#include "AWToolSDK.h"
#include <windows.h>

extern "C" {
    _declspec(dllexport) DWORD NvOptimusEnablement= 0x00000001;
}

AlienFan_SDK::Control* controller = nullptr;
DWORD controllerRefCount = 0;
AlienFan_SDK::Control* getController() {
    if (::controller == nullptr) {
        ::controller = new AlienFan_SDK::Control();
#ifdef _DEBUG
        printf("Run controller probe!\n");
#endif // 
        controller->Probe();
#ifdef _DEBUG
        printf("SDK initialize complete!\n");
#endif // 
    } 
    controllerRefCount += 1;
    return ::controller;
}
void releaseController() {
    controllerRefCount -= 1;
    if (controllerRefCount <= 0) {
        controller->~Control();
        controller = nullptr;
    }
}

#ifdef ALIEN_FAN_SDK
FanControl::FanControl()
{   
    this->controller = getController();
}

FanControl::~FanControl()
{
    releaseController();
    this->controller = nullptr;
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
LONG FanControl::getFanBoost(BYTE index)
{
    return this->controller->GetFanBoost(index);
}
LONG FanControl::unlockFanControl()
{
    return this->controller->Unlock();
}
DWORD FanControl::setFan(BYTE index, DWORD value)
{
    return this->controller->SetFanBoost(index,(BYTE)(value & 0xff));
}
#endif // ALIEN_FAN_SDK

int32_t testfct()
{
    return 42;
}
#ifdef ALIEN_POWER_SDK
PowerControl::PowerControl()
{
    this->controller = getController();
}

PowerControl::~PowerControl()
{
    releaseController();
    this->controller = nullptr;
}

BYTE PowerControl::getPower(DWORD index)
{
    return this->controller->powers[index];
}

BYTE PowerControl::getPowersCount(DWORD index)
{
    return this->controller->powers.size();
}

BYTE PowerControl::getCurPower(bool isRtnRaw = false)
{
    return this->controller->GetPower(isRtnRaw);
}

LONG PowerControl::setPower(DWORD value, bool isRaw)
{
    if (isRaw == true) {
        return this->controller->SetPower(value);
    }
    if (value >= this->controller->powers.size())return -1;
    return this->controller->SetPower(this->controller->powers[value]);
}
#endif
#ifdef ALIEN_Graphic_SDK
GraphicControl::GraphicControl()
{
}

GraphicControl::~GraphicControl()
{
}

void staticSetGraphicOptimus(bool enable) {
    if (enable = true) {
        NvOptimusEnablement = 0x00000001;
    }
    else
    {
        NvOptimusEnablement = 0x00000000;
    }
}
void GraphicControl::setGraphicOptimus(bool enable)
{
    staticSetGraphicOptimus(enable);
}
#endif


