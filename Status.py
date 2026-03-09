from .Items import VirtualDisks, HardDrives, PCIeCards, Services, Towers, Mounts
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.time import sleep

def LogStatus(
    name: str,
    connected: bool
) -> None:

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

    print('\nMounts:')
    for mount in Mounts:
        LogStatus(
            name = mount.path,
            connected = mount.exists
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
            name = str(s.path),
            connected = s.running
        )

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, True)
