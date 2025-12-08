from __init__ import devices, LogStatus, services
from philh_myftp_biz.text import abbreviate
from philh_myftp_biz.pc import pause, cls
from philh_myftp_biz.time import sleep

while True:

    cls()

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

    print('\nServices:')
    for s in services:

        mod, path = s.split('/')

        LogStatus(
            name = abbreviate(4, mod, True, '.') + '/' + path,
            connected = services[s].Running()
        )

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, True)