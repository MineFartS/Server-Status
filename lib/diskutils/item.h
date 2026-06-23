#pragma once

#include <iostream>

struct HardwareItem {

    virtual bool Connected() {return false;};
    
    virtual std::string disk_path() {return "";};
    virtual std::string disk_num() {return "";};

    virtual void cleanup() {};

    virtual std::string FriendlyName() {return "";};
    virtual void setFriendlyName(std::string name) {};

    virtual std::string Usage() {return "";};
    virtual void setUsage(std::string usage) {};

};
