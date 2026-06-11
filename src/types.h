#include <string>
#include <vector>
#include <optional>
#include <variant>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <nlohmann/json.hpp> // Assuming nlohmann/json for JSON handling

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
    mutable std::optional<std::string> _cached_name;
    mutable std::optional<json> _cached_physical_disk;
    mutable std::optional<json> _cached_wmi_object;
    mutable std::optional<std::string> _cached_unique_id;
    mutable std::optional<std::string> _cached_reg_path;

    std::string name() const {
        if (!_cached_name) {
            char buf[50];
            snprintf(buf, sizeof(buf), "%02d-%s [%s]", id, tower.c_str(), conn.c_str());
            _cached_name = std::string(buf);
        }
        return *_cached_name;
    }

    std::optional<json> physicalDisk() const {
        if (!_cached_physical_disk) {
            try {
                json data = RunHidden(
                    "Get-PhysicalDisk -SerialNumber " + sn + " | ConvertTo-Json",
                    "ps"
                ).output("json");

                if (data.is_array() && !data.empty()) {
                    _cached_physical_disk = data[0];
                } else {
                    _cached_physical_disk = data;
                }
            } catch (const std::runtime_error&) {
                _cached_physical_disk = std::nullopt;
            }
        }
        return _cached_physical_disk;
    }

    std::optional<json> wmiObject() const {
        if (!_cached_wmi_object) {
            try {
                std::vector<std::string> cmd = {
                    "Get-WmiObject", "-Query",
                    "SELECT * FROM Win32_DiskDrive WHERE SerialNumber = '" + sn + "'",
                    "| ConvertTo-Json"
                };
                _cached_wmi_object = RunHidden(cmd, "ps").output("json");
            } catch (const std::runtime_error&) {
                _cached_wmi_object = std::nullopt;
            }
        }
        return _cached_wmi_object;
    }

    std::optional<std::string> uniqueId() const {
        if (!_cached_unique_id) {
            auto pd = physicalDisk();
            if (pd && pd->contains("UniqueId")) {
                _cached_unique_id = (*pd)["UniqueId"].get<std::string>();
            }
        }
        return _cached_unique_id;
    }

    bool connected() {
        clear_cache(this);
        _cached_physical_disk.reset(); // Manual clear for this implementation

        auto fn = friendlyName();
        if (fn) {
            auto pd = physicalDisk();
            if (pd && pd->contains("OperationalStatus")) {
                std::string opStatus = (*pd)["OperationalStatus"].get<std::string>();
                return (opStatus != "Lost Communication");
            }
        }
        return false;
    }

    std::optional<std::string> regPath() const {
        if (!_cached_reg_path) {
            auto wmi = wmiObject();
            if (wmi && wmi->contains("PNPDeviceID")) {
                std::string pnpId = (*wmi)["PNPDeviceID"].get<std::string>();
                _cached_reg_path = "HKLM:SYSTEM\\ControlSet001\\Enum\\" + pnpId;
            }
        }
        return _cached_reg_path;
    }

    // FriendlyName
    std::optional<std::string> friendlyName() const {
        auto pd = physicalDisk();
        if (pd && pd->contains("FriendlyName")) {
            std::string fn = (*pd)["FriendlyName"].get<std::string>();
            if (!fn.empty()) {
                return fn;
            }
        }
        return std::nullopt;
    }

    void setFriendlyName(std::string name_val) {
        if (name_val != friendlyName().value_or("")) {
            auto uid = uniqueId();
            if (uid) {
                RunHidden(
                    "Set-PhysicalDisk -UniqueId '" + *uid + "' -NewFriendlyName '" + name_val + "'",
                    "ps"
                );
            }

            auto rp = regPath();
            if (rp) {
                RunHidden(
                    "Set-ItemProperty '" + *rp + "' FriendlyName '" + name() + "'",
                    "ps"
                );
            }

            clear_cache(this);
            _cached_physical_disk.reset();
            _cached_name.reset();
            _cached_unique_id.reset();
            _cached_reg_path.reset();
        }
    }

    // Usage
    std::optional<std::string> usage() const {
        auto pd = physicalDisk();
        if (pd && pd->contains("Usage")) {
            return (*pd)["Usage"].get<std::string>();
        }
        return std::nullopt;
    }

    void setUsage(std::string usage_val) {
        if (usage_val != usage().value_or("")) {
            auto uid = uniqueId();
            if (uid) {
                RunHidden(
                    "Set-PhysicalDisk -UniqueId '" + *uid + "' -Usage " + usage_val,
                    "ps"
                );
            }

            clear_cache(this);
            _cached_physical_disk.reset();
        }
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
