#include <string>
#include <vector>
#include <optional>
#include <variant>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <nlohmann/json.hpp>
#include <windows.h>
#include <winioctl.h>
#include <comdef.h>
#include <WbemIdl.h>
#include <initguid.h>
#include <cfgmgr32.h>
#include <devguid.h>
#include <devpkey.h>

#pragma comment(lib, "wbemuuid.lib")
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "cfgmgr32.lib")

struct HardDrive {
    std::string sn;

    //===============================================================================
    // Helper functions to trim whitespaces
    
    std::string trim_serial_number(const std::string& str) {
        size_t first = str.find_first_not_of(" \t\r\n");
        if (first == std::string::npos) return "";
        size_t last = str.find_last_not_of(" \t\r\n");
        return str.substr(first, (last - first + 1));
    }

    std::string trim_hardware_descriptor(const char* cstr) {
        if (!cstr) return "";
        std::string str(cstr);
        size_t end = str.find_last_not_of(" \t\r\n");
        return (end == std::string::npos) ? "" : str.substr(0, end + 1);
    }

    //===============================================================================
    // DrivePath

    mutable std::optional<std::string> _cached_drive_path;

    std::string _drivePath() {
        
        // Windows supports up to 16 or more drives normally; loop through a reasonable index range
        for (UINT driveIndex = 0; driveIndex < 50; ++driveIndex) {
            std::string drivePath = "\\\\.\\PhysicalDrive" + std::to_string(driveIndex);
            
            // Open handle to the physical drive
            HANDLE hDevice = CreateFileA(
                drivePath.c_str(),
                0, // No access rights required to read attributes
                FILE_SHARE_READ | FILE_SHARE_WRITE,
                NULL,
                OPEN_EXISTING,
                0,
                NULL
            );

            if (hDevice == INVALID_HANDLE_VALUE) {
                continue; // Drive index doesn't exist, move to next
            }

            // Configure the query to fetch device properties
            STORAGE_PROPERTY_QUERY propertyQuery = {};
            propertyQuery.PropertyId = StorageDeviceProperty;
            propertyQuery.QueryType = PropertyStandardQuery;

            // Allocate a buffer to hold the output descriptor block
            BYTE outputBuffer[1024] = {};
            DWORD bytesReturned = 0;

            // Send the IOCTL command to the physical disk
            BOOL result = DeviceIoControl(
                hDevice,
                IOCTL_STORAGE_QUERY_PROPERTY,
                &propertyQuery,
                sizeof(propertyQuery),
                outputBuffer,
                sizeof(outputBuffer),
                &bytesReturned,
                NULL
            );

            CloseHandle(hDevice);

            if (result) {
                STORAGE_DEVICE_DESCRIPTOR* deviceDescriptor = reinterpret_cast<STORAGE_DEVICE_DESCRIPTOR*>(outputBuffer);
                
                // Check if a valid serial number offset exists
                if (deviceDescriptor->SerialNumberOffset != 0 && deviceDescriptor->SerialNumberOffset < bytesReturned) {
                    // Extract the null-terminated ASCII serial number string
                    const char* rawSerial = reinterpret_cast<const char*>(outputBuffer + deviceDescriptor->SerialNumberOffset);
                    std::string currentSerial = trim_serial_number(rawSerial);

                    // Check for a match (case-insensitive or exact depending on preference)
                    if (currentSerial == sn) {
                        return drivePath; // Found a match!
                    }
                }
            }
        }
        return ""; // No matching serial number found
    }

    std::string DrivePath() {
        if (!_cached_drive_path)
            _cached_drive_path = _drivePath();
        
        return *_cached_drive_path;
    }

    //===============================================================================
    // FriendlyName

    // Retrieves the actual Windows Registry FriendlyName for a specific \\.\PhysicalDriveX path
    std::string FriendlyName() {
        return ""; // TODO
    }

    void setFriendlyName(std::string name) {
        // TODO
    }

    //===============================================================================
    // Connected
    
    bool Connected() {
        return DrivePath() != "";
    }

    //===============================================================================
    // Usage

    std::string Usage() {
        return ""; // TODO
    }

    void setUsage(std::string usage) {
        // TODO
    }

    //===============================================================================

};
