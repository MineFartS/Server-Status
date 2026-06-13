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
#include <setupapi.h>

#pragma comment(lib, "wbemuuid.lib")
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "cfgmgr32.lib")
#pragma comment(lib, "setupapi.lib")

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

    mutable std::string _cached_drive_path = "";

    std::string DrivePath() {
 
        if (!_cached_drive_path.empty())
            return _cached_drive_path;

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
                        _cached_drive_path = drivePath;
                        return _cached_drive_path;
                    }
                }
            }
        }
        
        return _cached_drive_path; // No matching serial number found
    }

    //===============================================================================
    // DiskNumber

    std::string DiskNumber() {
    
        const std::string prefix = "\\.\\PhysicalDrive";
    
        if (DrivePath().rfind(prefix, 0) == 0) {
            return DrivePath().substr(prefix.size());
        }

        return "";
    }

    //===============================================================================
    // FriendlyName

    std::string FriendlyName() {
        if (DrivePath().empty()) return "";

        std::string diskNumber = DiskNumber();

        static const GUID GUID_DEVCLASS_DISKDRIVE = { 0x4D36E967, 0xE325, 0x11CE, { 0xBF, 0xC1, 0x08, 0x00, 0x2B, 0xE1, 0x03, 0x18 } };

        HDEVINFO hDevInfo = SetupDiGetClassDevs(&GUID_DEVCLASS_DISKDRIVE, NULL, NULL, DIGCF_PRESENT);
        if (hDevInfo == INVALID_HANDLE_VALUE) return "";

        std::string result;
        SP_DEVINFO_DATA devInfoData;
        devInfoData.cbSize = sizeof(SP_DEVINFO_DATA);

        for (DWORD i = 0;; ++i) {
            if (!SetupDiEnumDeviceInfo(hDevInfo, i, &devInfoData)) break;

            char instanceId[512] = { 0 };
            if (!SetupDiGetDeviceInstanceIdA(hDevInfo, &devInfoData, instanceId, (DWORD)sizeof(instanceId), NULL)) {
                continue;
            }

            if (!diskNumber.empty()) {
                std::string inst(instanceId);
                if (inst.find("PhysicalDrive") == std::string::npos || inst.find(diskNumber) == std::string::npos) {
                    continue;
                }
            }

            WCHAR wideName[512] = { 0 };
            DWORD propType = 0;
            ULONG outLen = (ULONG)sizeof(wideName);
            if (CM_Get_DevNode_Registry_PropertyW(devInfoData.DevInst, CM_DRP_FRIENDLYNAME, &propType, (PVOID)wideName, &outLen, 0) == CR_SUCCESS) {
                int len = WideCharToMultiByte(CP_UTF8, 0, wideName, -1, NULL, 0, NULL, NULL);
                if (len > 0) {
                    std::string utf8((size_t)len - 1, '\0');
                    WideCharToMultiByte(CP_UTF8, 0, wideName, -1, utf8.data(), len, NULL, NULL);
                    result = utf8;
                    break;
                }
            }
        }

        SetupDiDestroyDeviceInfoList(hDevInfo);
        return result;
    }

    void setFriendlyName(std::string name) {

        std::string ps_cmd = "powershell.exe -Command \"Get-PhysicalDisk | Where-Object SerialNumber -eq '"+sn+"' | Set-PhysicalDisk -NewFriendlyName '"+name+"'\"";

        std::system(ps_cmd.c_str());

        if (DrivePath().empty()) return;

        std::string diskNumber = DiskNumber();

        static const GUID GUID_DEVCLASS_DISKDRIVE = { 0x4D36E967, 0xE325, 0x11CE, { 0xBF, 0xC1, 0x08, 0x00, 0x2B, 0xE1, 0x03, 0x18 } };

        HDEVINFO hDevInfo = SetupDiGetClassDevs(&GUID_DEVCLASS_DISKDRIVE, NULL, NULL, DIGCF_PRESENT);
        if (hDevInfo == INVALID_HANDLE_VALUE) return;

        // Convert UTF-8 input to UTF-16 for the CM_* calls.
        int wideLen = MultiByteToWideChar(CP_UTF8, 0, name.c_str(), -1, NULL, 0);
        if (wideLen <= 0) {
            SetupDiDestroyDeviceInfoList(hDevInfo);
            return;
        }
        std::vector<WCHAR> wideName((size_t)wideLen);
        MultiByteToWideChar(CP_UTF8, 0, name.c_str(), -1, wideName.data(), wideLen);

        SP_DEVINFO_DATA devInfoData;
        devInfoData.cbSize = sizeof(SP_DEVINFO_DATA);

        for (DWORD i = 0;; ++i) {
            if (!SetupDiEnumDeviceInfo(hDevInfo, i, &devInfoData)) break;

            char instanceId[512] = { 0 };
            if (!SetupDiGetDeviceInstanceIdA(hDevInfo, &devInfoData, instanceId, (DWORD)sizeof(instanceId), NULL)) {
                continue;
            }

            if (!diskNumber.empty()) {
                std::string inst(instanceId);
                if (inst.find("PhysicalDrive") == std::string::npos || inst.find(diskNumber) == std::string::npos) {
                    continue;
                }
            }

            // Apply the FriendlyName registry property for this device.
            // Data buffer must include the terminating null.
            ULONG dataSize = (ULONG)(wideName.size() * sizeof(WCHAR));
            // Property length is in bytes for the CM_* function.
            // Using 0 for flags (default).
            (void)CM_Set_DevNode_Registry_PropertyW(
                devInfoData.DevInst,
                CM_DRP_FRIENDLYNAME,
                wideName.data(),
                dataSize,
                0);
            break;
        }

        SetupDiDestroyDeviceInfoList(hDevInfo);
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
