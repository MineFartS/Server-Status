
$ucrt64 = "$PSScriptRoot\msys2\ucrt64"

function Invoke-GPP {
    param(
        [Parameter(ValueFromRemainingArguments)]
        $cmdargs
    )

    $prevloc = Get-Location

    Set-Location "$ucrt64\bin\"

    .\g++.exe @cmdargs

    Set-Location $prevloc
    
}

function Repair-Environment {

    Set-Location $PSScriptRoot

    git.exe submodule update --init --recursive --remote

}

Export-ModuleMember `
    -Function * `
    -Variable *
