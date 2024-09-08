#include <pybind11/pybind11.h>
#include "AWToolSDK.h"

namespace py = pybind11;

PYBIND11_MODULE(AWToolSDK, m) {
#ifdef ALIEN_FAN_SDK //SDK中添加风扇控制函数
    py::class_<FanControl>(m, "FanControl")
        .def(py::init<>())
        .def("checkAPI", &FanControl::checkAPI); 
#endif //ALIEN_FAN_SDK
    m.def("testfct", &testfct);
}