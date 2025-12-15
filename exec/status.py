from philh_myftp_biz.text import abbreviate
from philh_myftp_biz.time import sleep
from philh_myftp_biz.pc import cls

from items.Virtual_Disks import VirtualDisks
from items.Hard_Drives import HardDrives
from items.PCIe_Cards import PCIeCards
from items.Services import Services
from items.Towers import Towers

def LogStatus(
    name: str,
    connected: bool
):
    from philh_myftp_biz.text import abbreviate
    from philh_myftp_biz.pc import print

    fname = abbreviate(12, name, end='.').ljust(12, ' ')

    print(
        f'   {fname} : ',
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

        sname = abbreviate(
            num = 4,
            string = s.module.name,
            end = '.'
        )

        LogStatus(
            name = sname + s.path,
            connected = s.Running()
        )

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, True)