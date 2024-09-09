﻿#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <comutil.h>
#include "AWToolSDK.h"

static OLECHAR *stringToOlechar(const std::string str)
{
    size_t len = str.length() + 1;
    OLECHAR *oleStr = new OLECHAR[len];
    size_t convertedChars = 0;
    mbstowcs_s(&convertedChars, oleStr, len, str.c_str(), _TRUNCATE);
    return oleStr;
}
namespace py = pybind11;

PYBIND11_MODULE(pyAWToolSDK, m)
{
#ifdef ALIEN_FAN_SDK // SDK中添加风扇控制函数
    m.doc() = u8"此类用于控制Alienware机器的风扇，提供切换电源模式等功能";
    // 添加传感器信息结构类
    py::class_<AlienFan_SDK::ALIENFAN_SEN_INFO>(m, "Sensor_info", u8"传感器属性")
        .def(py::init<>())
        .def_readwrite("index", &AlienFan_SDK::ALIENFAN_SEN_INFO::index)             // 风扇代码
        .def_readwrite("type", &AlienFan_SDK::ALIENFAN_SEN_INFO::type)               // 风扇种类
        .def_readwrite("name", &AlienFan_SDK::ALIENFAN_SEN_INFO::name)               // 名称
        .def_property("instance",                                                    // for ESIF/OHM/SSD sensors
                      [](AlienFan_SDK::ALIENFAN_SEN_INFO info) -> pybind11::object { // get
                          return py::cast<std::wstring>(info.instance, py::return_value_policy::take_ownership);
                      },
                      [](AlienFan_SDK::ALIENFAN_SEN_INFO info, std::string value) { // set
                          SysFreeString(info.instance);
                          OLECHAR *str = stringToOlechar(value);
                          info.instance = SysAllocString(str);
                          delete[] str;
                      })
        .def_property("valueName",
                      [](AlienFan_SDK::ALIENFAN_SEN_INFO info) -> pybind11::object { // get
                          return py::cast<std::wstring>(info.valueName, py::return_value_policy::take_ownership);
                      },
                      [](AlienFan_SDK::ALIENFAN_SEN_INFO info, std::string value) { // set
                          SysFreeString(info.valueName);
                          OLECHAR *str = stringToOlechar(value);
                          info.valueName = SysAllocString(str);
                          delete[] str;
                      });

    // 添加风扇信息结构类
    py::class_<AlienFan_SDK::ALIENFAN_FAN_INFO>(m, "Fan_info", u8"风扇属性")
        .def(py::init<>())
        .def_readwrite("id", &AlienFan_SDK::ALIENFAN_FAN_INFO::id,u8"风扇fanID")
        .def_readwrite("type", &AlienFan_SDK::ALIENFAN_FAN_INFO::type,u8"风扇类别");

    py::class_<FanControl>(m, "Fan_controller")
        .def(py::init<>())
        .def("checkAPI", &FanControl::checkAPI)
        .def("getFan", &FanControl::getFan, u8"获取风扇的id和type")
        //.def("getSensor", &FanControl::getSensor);
        .def("getMAXFan", &FanControl::getMAXFan, u8"返回风扇总数，以风扇数量作为index用getFan函数获取风扇id和风扇类别")
        .def("getFansCount", &FanControl::getFansCount, u8"返回风扇总数，以风扇数量作为index用getFan函数获取风扇id和风扇类别")
        .def("getFanRPM", &FanControl::getFanRPM, u8"获取指定风扇的当前转速")
        .def("unlockFanControl", &FanControl::unlockFanControl, "解锁自行控制风扇，切换到自定义电源模式")
        .def("setFan", &FanControl::setFan,u8"设置风扇转速，value指定于0-255");

#endif // ALIEN_FAN_SDK
    m.def("testfct", &testfct);
}