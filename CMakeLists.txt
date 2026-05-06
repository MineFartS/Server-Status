cmake_minimum_required(VERSION 3.20)
project(ScriptsCPP LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(ScriptsCPP
    src/main.cpp
    src/util/json_utils.cpp
)

target_include_directories(ScriptsCPP PRIVATE src)

# Note: JSON parsing uses a header-only library if you add one.
# For now, we keep json_utils minimal and only implement what this repo needs.

