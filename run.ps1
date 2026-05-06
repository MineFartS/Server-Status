param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Module
)

# Optional positional args for compatibility with the old VBS:
# run.ps1 <Module> [Visible] [Verbose]
$Visible = $true
$Verbose = $false

if ($args.Count -ge 1) { $Visible = [bool]$args[1] }
if ($args.Count -ge 2) { $Verbose = [bool]$args[2] }

$exe = 'C:\Scripts_CPP\ScriptsCPP.exe'

function Build-Cpp {
    $buildDir = 'build'
    $gen = "Visual Studio 17 2022"
    $arch = 'x64'

    $cmake = $null
    $cmakeCmd = Get-Command cmake -ErrorAction SilentlyContinue
    if ($cmakeCmd) {
        $cmake = 'cmake'
    } else {
        $fallback = 'C:\ProgramData\chocolatey\bin\cmake.exe'
        if (Test-Path $fallback) { $cmake = $fallback }
    }

    if (-not $cmake) {
        Write-Host 'cmake not found on PATH and fallback cmake.exe not found; cannot build.'
        return $false
    }

    Write-Host "Building via $cmake..."
    & $cmake -S . -B $buildDir -G $gen -A $arch
    if ($LASTEXITCODE -ne 0) { return $false }

    & $cmake --build $buildDir --config Release
    return ($LASTEXITCODE -eq 0)
}

if (-not (Test-Path $exe)) {
    Push-Location 'C:\Scripts_CPP'
    try {
        $ok = Build-Cpp
        if (-not $ok) {
            exit 1
        }
    }
    finally {
        Pop-Location
    }
}

Push-Location 'C:\Scripts_CPP'
try {
    $cmd = @($exe, $Module)
    if ($Verbose) { $cmd += '-v' }

    # Visible maps to PowerShell window via Start-Process
    if ($Visible) {
        & $cmd
    } else {
        Start-Process -FilePath $exe -ArgumentList @($Module, (if($Verbose){'-v'})) -WindowStyle Hidden -Wait
    }
}
finally {
    Pop-Location
}

