#include <iostream>
#include <string>
#include <nlohmann/json.hpp>
#include <hdd.h>
#include <item.h>
#include <any>

using namespace std::string_literals;

// type = argv[1]; argc=2
// id   = argv[2]; argc=3
// prop = argv[3]; argc=4
// val  = argv[4]; argc=5

int main(int argc, char** argv) {

    HardwareItem* item;

    if (argv[1] == "disk"s) {
        HardDrive hdd = HardDrive(argv[2]);
        item = &hdd;
    }

    nlohmann::json outp;
    outp["result"] = nullptr;

    if (argc == 4) { // Get Value

        if (argv[3] == "FriendlyName"s) {
            outp["result"] = item->FriendlyName();
        
        } else if (argv[3] == "Connected"s) {
            outp["result"] = item->Connected();

        } else if (argv[3] == "disk_path"s) {
            outp["result"] = item->disk_path();

        } else if (argv[3] == "disk_num"s) {
            outp["result"] = item->disk_num();
        
        } else if (argv[3] == "Usage"s) {
            outp["result"] = item->Usage();
        }

    } else { // Set Value

        if (argv[3] == "FriendlyName"s) {
            item->setFriendlyName(argv[4]);

        } else if (argv[3] == "Usage"s) {
            item->setUsage(argv[4]);
        }

    }

    item->cleanup();

    if (outp["result"] == "") {
        outp["result"] = nullptr;
    }

    std::cout << outp.dump(4) << std::endl;

    return 0;
}

