param(
    [Switch] $Force
)

git.exe submodule update --init --recursive --remote

$prevloc = Get-Location

# FIX: Convert the relative path to an absolute path before changing directory
$python = (Get-Item "$PSScriptRoot\..\python314").FullName

Set-Location "$PSScriptRoot\..\msys2\ucrt64\bin"

$outp = "C:/Scripts/Items/_cpp.pyd"

if ($Force) {
    Remove-Item $outp -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $outp)) {

    .\g++.exe `
        -O3 -shared -std=c++17 -fPIC `
        -I"$python\include" `
        -I"$PSScriptRoot" `
        "$PSScriptRoot/main.cpp" `
        -o "$outp" `
        -L"$python\libs" `
        -lpython314 `
        -lsetupapi `
        -lcfgmgr32

}

Set-Location $prevloc
