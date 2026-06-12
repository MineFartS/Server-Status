#include <iostream>
#include <string>
#include <hdd.h>
#include <nlohmann/json.hpp>

int main(int argc, char** argv) {

    nlohmann::json outp;
    outp["result"] = nullptr;

    HardDrive hdd = HardDrive(argv[1]);

    std::string property = argv[2];

    if (argc == 3) { // Get Value

        if (property == "FriendlyName") {
            outp["result"] = hdd.FriendlyName();
        
        } else if (property == "Connected") {
            outp["result"] = hdd.Connected();
        
        } else if (property == "Usage") {
            outp["result"] = hdd.Usage();
        
        }

    } else if (argc == 4) { // Set Value

        std::string value = argv[3];

        if (property == "FriendlyName") {
            hdd.setFriendlyName(value);

        } else if (property == "Usage") {
            hdd.setUsage(value);
        }

    }

    if (outp["result"] == "") {
        outp["result"] = nullptr;
    }

    std::cout << outp.dump(4) << std::endl;

    return 0;
}

