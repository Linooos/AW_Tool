#include "pybind11/pybind11.h"
#include "ctype.h"

int32_t testFunc() {
	return 42;
}

namespace py = pybind11;

PYBIND11_MODULE(testMod, m) {
	m.def("testFunc", &testFunc);
}