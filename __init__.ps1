
Set-Location $PSScriptRoot

function diskConnected($SerialNumber) {

    $Disk = Get-PhysicalDisk -SerialNumber $SerialNumber

    if ($Disk.FriendlyName.Length -gt 0) {
        try {
            return (($Disk.OperationalStatus -join '') -ne 'Lost Communication')
        } catch {
            return $False 
        }
    } else {
        return $False
    }

}

$HardDrives = @{}

$__SerialNumbers = (Get-Content "./Hard Drives.json" | ConvertFrom-Json)

$__SerialNumbers.PSObject.Properties | ForEach-Object -Process {

    $BaseName = $_.Name

    $_.Value.PSObject.Properties | ForEach-Object -Process {

        if ($_.Value.Count -gt 0) {
            
            $HardDrives["$BaseName $($_.Name)"] = $_.Value

        }

    }

}

# ================================================================================================

$PCIeCards = @{}

$__DeviceIds = (Get-Content "./PCIe Cards.json" | ConvertFrom-Json)

$__DeviceIds.PSObject.Properties | ForEach-Object -Process {

    $PCIECards[$_.Name] = Get-PnpDevice -DeviceId $_.Value -ErrorAction SilentlyContinue

}

# ================================================================================================

function LogStatus {

    param(
        [string] $label,
        [bool] $connected
    )

    Write-Host '    ' $label.PadRight(15, ' ') ':: ' -NoNewline -ForegroundColor Cyan

    if ($connected) {

        Write-Host "Connected" -ForegroundColor Green

    } else {

        Write-Host "Missing" -ForegroundColor Red

    }

}