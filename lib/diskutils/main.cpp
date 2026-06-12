#include <iostream>
#include <string>
#include <hdd.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

int main(int argc, char** argv) {

    HardDrive hdd = HardDrive(argv[1]);

    json outp;
    outp["result"];

    std::string property = argv[2];
    
    if (argc == 4) { // Set Value
        
        if (property == "FriendlyName") {
            hdd.setFriendlyName(argv[4]);

        } else if (property == "Usage") {
            hdd.setUsage(argv[4]);
        }

    }
        
    if (property == "FriendlyName") {
        outp["result"] = hdd.FriendlyName();
    
    } else if (property == "Connected") {
        outp["result"] = hdd.Connected();
    
    } else if (property == "Usage") {
        outp["result"] = hdd.Usage();
    }

    if (outp["result"] == "") {
        outp["result"] = nullptr;
    }

    std::cout << outp.dump(4) << std::endl;

    return 0;
}

