#include <pybind11/pybind11.h>
#include <iostream>
#include <string>

namespace py = pybind11;

// Standard C++ class
class HardDrive {
public:

    // Property
    std::string name;

    // Constructor
    HardDrive(std::string name) : name(name) {}

    // Method
    std::string greet() {
        return "Hello, " + name + "!";
    }

};

// Create the Python bindings
PYBIND11_MODULE(main, m) {

    py::class_<HardDrive>(m, "HardDrive")
        .def(py::init<std::string>())             // Binds the constructor
        .def("greet", &HardDrive::greet)               // Binds the member method
        .def_readwrite("name", &HardDrive::name);      // Allows Python to read/write the property

}