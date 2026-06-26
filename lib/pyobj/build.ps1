param([Switch] $Force)

$prevloc = Get-Location
Set-Location "C:/Scripts/"

git.exe submodule update --init --recursive --remote

Set-Location "$PSScriptRoot\..\msys2\ucrt64\bin"

$outp = "C:/Scripts/Items/_cpp.pyd"

if ($Force) {
    Remove-Item $outp -Force -ErrorAction SilentlyContinue
}

$lib = (Get-Item "$PSScriptRoot\..\").FullName

if (-not (Test-Path $outp)) {

    .\g++.exe -v `
        -O3 -shared -std=c++17 -fPIC `
        -I"$lib/python314/include" `
        -I"$lib/pybind11/include" `
        -I"$lib/json/include" `
        -I"$PSScriptRoot" `
        "$PSScriptRoot/main.cpp" `
        -o "$outp" `
        -L"$lib/python314/libs" `
        -lpython314 `
        -lsetupapi `
        -lcfgmgr32

}

Set-Location $prevloc
