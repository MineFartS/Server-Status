param(
    [String] $Module,
    [Switch] $Hidden,
    [Switch] $Verbose
)

Import-Module "$PSScriptRoot/__mod__.psm1" -Force

Repair-Environment

$exe = "$ucrt64\bin\main.exe"

Remove-Item $exe -ErrorAction SilentlyContinue

Invoke-GPP `
    "$PSScriptRoot/src/main.cpp" `
    '-o' $exe `
    '-I' "$PSScriptRoot/src"

& $exe $Module
