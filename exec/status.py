from philh_myftp_biz.text import abbreviate
from philh_myftp_biz.time import sleep
from philh_myftp_biz.pc import cls

from Status_Items.Virtual_Disks import VirtualDisks
from Status_Items.Hard_Drives import HardDrives
from Status_Items.PCIe_Cards import PCIeCards
from Status_Items.Services import Services
from Status_Items.Towers import Towers

def LogStatus(
    name: str,
    connected: bool
):
    from philh_myftp_biz.text import abbreviate
    from philh_myftp_biz.pc import print

    fname = name.ljust(35, '.')

    print(
        f'   {fname}: ',
        end = ''
    )

    if connected:
        print(
            'Active',
            color = 'GREEN'
        )
    else:
        print(
            'Inactive',
            color = 'RED'
        )

while True:

    cls()

    print("\n|-----------------------------------| Server Status |-----------------------------------|\n")    

    print('\nHard Drives:')
    for device in HardDrives:
        LogStatus(
            name = device.Name,
            connected = device.Connected
        )

    print('\nPCIe Cards:')
    for device in PCIeCards:
        LogStatus(
            name = device.Name,
            connected = device.Connected
        )

    print('\nVirtual Disks:')
    for device in VirtualDisks:
        LogStatus(
            name = device.Name,
            connected = device.Connected
        )

    print('\nTowers:')
    for device in Towers:
        LogStatus(
            name = device.Name,
            connected = device.Connected
        )

    print('\nServices:')
    for s in Services:

        LogStatus(
            name = s.path,
            connected = s.Running()
        )

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, True)
