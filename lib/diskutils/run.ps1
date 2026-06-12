
git.exe submodule update --init --recursive --remote

Set-Location "$PSScriptRoot\..\msys2\ucrt64\bin"

if (-not (Test-Path "main.exe")) {
    .\g++.exe `
        "$PSScriptRoot/main.cpp" `
        '-o' "main.exe" `
        '-I' $PSScriptRoot
}

.\main.exe @args
