param(
    [Switch] $Force
)

git.exe submodule update --init --recursive --remote

$prevloc = Get-Location

Set-Location "$PSScriptRoot\..\msys2\ucrt64\bin"

if ($Force) {
    Remove-Item "main.exe" -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path "main.exe")) {
    .\g++.exe `
        "$PSScriptRoot/main.cpp" `
        '-o' "main.exe" `
        '-I' $PSScriptRoot `
        '-lsetupapi' `
        '-lcfgmgr32'
}


.\main.exe @args

Set-Location $prevloc