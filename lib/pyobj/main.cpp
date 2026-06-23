#include <pybind11/pybind11.h>
#include <iostream>
#include <string>
#include <hdd.h>

namespace py = pybind11;

// Create the Python bindings
PYBIND11_MODULE(main, m) {

    py::class_<HardDrive>(m, "HardDrive")
        
        .def(py::init<std::string>()) // Binds the constructor

        .def_readonly("Connected", &HardDrive::Connected)
        
        .def_property("FriendlyName", &HardDrive::FriendlyName, &HardDrive::setFriendlyName)

        .def_property("Usage", &HardDrive::Usage, &HardDrive::setUsage);

}