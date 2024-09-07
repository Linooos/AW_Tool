#include "pch.h"
#include <pybind11/pybind11.h>
#include "AWToolSDK.h"

namespace py = pybind11;

PYBIND11_MODULE(fanctrl, m) {
    py::class_<FanControl>(m, "FanControl")
        .def(py::init<>())
        .def("checkAPI", &FanControl::checkAPI);       
}