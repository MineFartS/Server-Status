from __init__ import devices, LogStatus
from philh_myftp_biz.pc import pause

print("\n|-----------------------------------| Server Status |-----------------------------------|\n")

print('\nHard Drives:')
for device in devices.HardDrives:
    LogStatus(
        name = device.Name,
        connected = device.Connected
    )

print('\nPCIe Cards:')
for device in devices.PCIeCards:
    LogStatus(
        name = device.Name,
        connected = device.Connected
    )

print('\nVirtual Disks:')
for device in devices.VirtualDisks:
    LogStatus(
        name = device.Name,
        connected = device.Connected
    )

print('\nTowers:')
for device in devices.Towers:
    LogStatus(
        name = device.Name,
        connected = device.Connected
    )

print("\n|---------------------------------------------------------------------------------------|\n")

pause()