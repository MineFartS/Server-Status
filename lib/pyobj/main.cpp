#include <pybind11/pybind11.h>
#include <iostream>
#include <string>
#include <hdd.h>

namespace py = pybind11;

// Create the Python bindings
PYBIND11_MODULE(main, m) {

    py::class_<HardDrive>(m, "HardDrive")

        .def(py::init<
            std::string, std::string, 
            int, std::string
        >(),
            py::arg("Tower"), 
            py::arg("Conn"), 
            py::arg("ID"), 
            py::arg("SN")
        )

        .def_readonly("Connected", &HardDrive::Connected)

        .def_readonly("Tower", &HardDrive::Tower)

        .def_readonly("Conn", &HardDrive::Conn)

        .def_readonly("ID", &HardDrive::ID)

        .def_readonly("Name", &HardDrive::Name)
        
        .def_property("FriendlyName", &HardDrive::FriendlyName, &HardDrive::setFriendlyName)

        .def_property("Usage", &HardDrive::Usage, &HardDrive::setUsage);

}