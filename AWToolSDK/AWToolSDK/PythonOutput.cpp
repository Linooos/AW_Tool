#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <comutil.h>
#include "AWToolSDK.h"

static OLECHAR *stringToOlechar(const std::string str)
{
    size_t len = str.length() + 1;
    OLECHAR *oleStr = new OLECHAR[len];
    mbstowcs(oleStr, str.c_str(), len);
    return oleStr;
}
namespace py = pybind11;

PYBIND11_MODULE(AWToolSDK, m)
{
#ifdef ALIEN_FAN_SDK // SDK中添加风扇控制函数
    m.doc() = string("此类用于控制Alienware机器的风扇，提供切换电源模式等功能");
    // 添加传感器信息结构类
    py::class_<AlienFan_SDK::ALIENFAN_SEN_INFO>(m, "Sensor_info", string("传感器属性")
        .def(py::init<>())
        .def_readwrite("index", &AlienFan_SDK::ALIENFAN_SEN_INFO::index)//风扇代码
        .def_readwrite("type", &AlienFan_SDK::ALIENFAN_SEN_INFO::type)//风扇种类
        .def_readwrite("name", &AlienFan_SDK::ALIENFAN_SEN_INFO::name)//名称
        .def_property("instance",//for ESIF/OHM/SSD sensors
            [](AlienFan_SDK::ALIENFAN_SEN_INFO info)-> pybind11::object{//get
        return py::cast<std::wstring>(info.instance, py::return_value_policy::take_ownership);
            },
            [](AlienFan_SDK::ALIENFAN_SEN_INFO info, std::string value) {//set
        SysFreeString(info.instance);
        OLECHAR *str = stringToOlechar(value);
        info.instance = SysAllocString(str);
        delete[] str;
            })
        .def_property("valueName", 
            [](AlienFan_SDK::ALIENFAN_SEN_INFO info)-> pybind11::object {//get
        return py::cast<std::wstring>(info.valueName, py::return_value_policy::take_ownership);
            }, 
            [](AlienFan_SDK::ALIENFAN_SEN_INFO info, std::string value) {//set
        SysFreeString(info.valueName);
        OLECHAR *str = stringToOlechar(value);
        info.valueName = SysAllocString(str);
        delete[] str;
            });

    //添加风扇信息结构类
    py::class_<AlienFan_SDK::ALIENFAN_FAN_INFO>(m, "Fan_info",string("风扇属性"))

        .def_readwrite("id", &AlienFan_SDK::ALIENFAN_FAN_INFO::id)
        .def_readwrite("typer", &AlienFan_SDK::ALIENFAN_FAN_INFO::type);


    py::class_<FanControl>(m, "FanControl",  string("风扇控制类")）
        .def(py::init<>())
        .def("checkAPI", &FanControl::checkAPI)
        .def("getFan",&FanControl::getFan)
        .def("getSensor", &FanControl::getSensor)

#endif // ALIEN_FAN_SDK
    m.def("testfct", &testfct);
}