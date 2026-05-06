#include <iostream>
#include <string>

static void print_usage() {
    std::cerr << "Usage: ScriptsCPP <Module> [visible] [verbose]\n"
              << "Modules: Interval.Startup | Interval.Hour | Interval.Week | Interval.Day\n";
}

int main(int argc, char** argv) {
    // Contract compatible with the existing run.vbs:
    // argv[0] = program
    // argv[1] = module name (e.g., Interval.Startup)
    // argv[2] = visible (bool)
    // argv[3] = verbose (bool)

    if (argc < 2) {
        print_usage();
        return 2;
    }

    std::string module = argv[1];

    bool visible = true;
    if (argc > 2 && argv[2]) {
        std::string v = argv[2];
        visible = (v == "true" || v == "1");
    }

    bool verbose = false;
    if (argc > 3 && argv[3]) {
        std::string v = argv[3];
        verbose = (v == "true" || v == "1");
    }

    if (verbose) {
        std::cout << "[ScriptsCPP] module=" << module
                  << " visible=" << (visible ? "true" : "false")
                  << " verbose=" << (verbose ? "true" : "false")
                  << std::endl;
    }

    if (module == "Interval.Startup") {
        std::cout << "[ScriptsCPP] Interval.Startup (stub)" << std::endl;
        return 0;
    }
    if (module == "Interval.Hour") {
        std::cout << "[ScriptsCPP] Interval.Hour (stub)" << std::endl;
        return 0;
    }
    if (module == "Interval.Week") {
        std::cout << "[ScriptsCPP] Interval.Week (stub)" << std::endl;
        return 0;
    }
    if (module == "Interval.Day") {
        std::cout << "[ScriptsCPP] Interval.Day (stub)" << std::endl;
        return 0;
    }

    std::cerr << "Unknown module: " << module << std::endl;
    print_usage();
    return 2;
}

