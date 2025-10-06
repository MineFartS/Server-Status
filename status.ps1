
while ($true) {

    # Import Objects
    . C:/Scripts/Devices/__init__.ps1

    Write-Output "|-----------------------------------| Server Status |-----------------------------------|"

    Write-Output ''
    Write-Output "Hard Drives:"

    # Check Disks
    $HardDrives.Keys | Sort-Object | ForEach-Object -Process {

        $disk = $HardDrives[$_]

        LogStatus `
            -label $_ `
            -connected ($disk.FriendlyName.Length -gt 0)

    }

    Write-Output ''
    Write-Output "PCIe Cards:"

    $PCIECards.Keys | Sort-Object | ForEach-Object -Process {

        $card = $PCIECards[$_]

        LogStatus `
            -label $_ `
            -connected ($card.Status -eq 'OK')

    }

    Write-Output ''
    Write-Output "|---------------------------------------------------------------------------------------|"
    Write-Output ''

    Read-Host 'Press Enter to Refresh ...'

    Clear-Host

}

