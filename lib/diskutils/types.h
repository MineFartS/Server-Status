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

#pragma comment(lib, "wbemuuid.lib")
#pragma comment(lib, "ole32.lib")

// Mocking external dependencies based on Python imports
// In a real scenario, these would be provided by the philh_myftp_biz C++ port
namespace philh_myftp_biz {
    namespace modules {
        class Service {
        public:
            std::string path;
            bool running;
            virtual ~Service() = default;
        };

        class Module {
        public:
            std::string path;
            bool exists;
            virtual ~Module() = default;
        };
    }

    namespace pc {
        struct Path {
            std::string path_str;
            bool exists() const {
                // Implementation for checking path existence
                return false; 
            }
        };
    }

    struct RunResult {
        std::string raw_output;
        nlohmann::json output(std::string format = "text") {
            if (format == "json") {
                try {
                    return nlohmann::json::parse(raw_output);
                } catch (...) {
                    throw std::runtime_error("JSONDecodeError");
                }
            }
            return nlohmann::json();
        }
    };

    RunResult Run(std::string command, std::string terminal = "cmd") {
        // Implementation for running command
        return RunResult();
    }

    RunResult RunHidden(std::variant<std::string, std::vector<std::string>> command, std::string terminal = "cmd") {
        // Implementation for running hidden command
        return RunResult();
    }

    void clear_cache(void* obj) {
        // Implementation for clearing cached properties
    }
}

using json = nlohmann::json;
using namespace philh_myftp_biz;

class Service : public modules::Service {
private:
    std::optional<std::string> _cached_name;

public:
    std::string name() {
        if (!_cached_name) {
            _cached_name = this->path;
        }
        return *_cached_name;
    }

    bool connected() const {
        return this->running;
    }
};

class Module : public modules::Module {
private:
    std::optional<std::string> _cached_name;

public:
    std::string name() {
        if (!_cached_name) {
            _cached_name = this->path;
        }
        return *_cached_name;
    }

    bool connected() const {
        return this->exists;
    }
};

struct VirtualDisk {
    std::string name;
    pc::Path mount;

    bool connected() const {
        return mount.exists();
    }

    void _ps(std::string cmd) {
        Run(
            cmd + "-VirtualDisk -FriendlyName '" + name + "'",
            "ps"
        );
    }

    void setConnected(bool connect) {
        if (connect) {
            // Connect-VirtualDisk
            _ps("Connect");

            // Repair-VirtualDisk
            _ps("Repair");
        } else {
            // Disconnect-VirtualDisk
            _ps("Disconnect");
        }
    }
};

struct HardDrive {    
    std::string tower;
    std::string conn; // Literal['SATA', 'USB', 'PROP']
    int id;
    std::string sn;

    // Cached properties
    mutable std::optional<std::string> _cached_drive_path;
    mutable std::optional<std::string> _cached_name;

    std::string name() const {
        if (!_cached_name) {
            char buf[50];
            snprintf(buf, sizeof(buf), "%02d-%s [%s]", id, tower.c_str(), conn.c_str());
            _cached_name = std::string(buf);
        }
        return *_cached_name;
    }

    // Helper function to trim whitespaces from serial numbers
    std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(" \t\r\n");
        if (first == std::string::npos) return "";
        size_t last = str.find_last_not_of(" \t\r\n");
        return str.substr(first, (last - first + 1));
    }

    std::string _drivePath() {

        // Standardize target string for comparison
        std::string target = trim(sn);
        
        // Windows supports up to 16 or more drives normally; loop through a reasonable index range
        for (UINT driveIndex = 0; driveIndex < 16; ++driveIndex) {
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
                    std::string currentSerial = trim(rawSerial);

                    // Check for a match (case-insensitive or exact depending on preference)
                    if (currentSerial == target) {
                        return drivePath; // Found a match!
                    }
                }
            }
        }
        return ""; // No matching serial number found
    }

    std::string drivePath() {
        if (!_cached_drive_path)
            _cached_drive_path = _drivePath();
        
        return *_cached_drive_path;
    }

    bool connected() {
        return drivePath() != "";
    }

    // Extracts the integer index "0" from "\\\\.\\PhysicalDrive0"
    int diskNum() {
        if (!connected()) return -1;

        std::string dp = drivePath();

        std::string strnum = dp.substr(dp.find_last_of("PhysicalDrive") + 1);

        return stoi(strnum);
    }

};

struct PCIeCard {
    std::variant<int, std::string> slot; // Literal[1, 2, 3, 4, 'M.2']
    int lanes; // Literal[1, 4, 16]
    std::string deviceId;

    mutable std::optional<std::string> _cached_name;
    mutable std::optional<json> _cached_pnp_device;

    std::string name() const {
        if (!_cached_name) {
            if (std::holds_alternative<int>(slot)) {
                _cached_name = "Slot " + std::to_string(std::get<int>(slot)) + " [x" + std::to_string(lanes) + "]";
            } else {
                _cached_name = std::get<std::string>(slot) + " [x" + std::to_string(lanes) + "]";
            }
        }
        return *_cached_name;
    }

    std::optional<json> pnpDevice() const {
        if (!_cached_pnp_device) {
            try {
                _cached_pnp_device = RunHidden(
                    "Get-PnpDevice -DeviceId '" + deviceId + "' | ConvertTo-Json",
                    "ps"
                ).output("json");
            } catch (const std::runtime_error&) {
                _cached_pnp_device = std::nullopt;
            }
        }
        return _cached_pnp_device;
    }

    bool connected() {
        clear_cache(this);
        _cached_pnp_device.reset();

        auto pnp = pnpDevice();
        if (pnp && pnp->contains("Status")) {
            return ((*pnp)["Status"].get<std::string>() == "OK");
        }
        return false;
    }
};

// Forward declaration for Tower
extern std::vector<HardDrive> HardDrives;

struct Tower {
    std::string id;

    mutable std::optional<std::string> _cached_name;

    std::string name() const {
        if (!_cached_name) {
            _cached_name = "Tower " + id;
        }
        return *_cached_name;
    }

    bool connected() {
        clear_cache(this);

        for (auto& hdd : HardDrives) {
            if (hdd.tower == id) {
                if (hdd.connected()) {
                    return true;
                }
            }
        }
        return false;
    }
};

// Global or external variable as referenced in Tower::Connected
std::vector<HardDrive> HardDrives;
