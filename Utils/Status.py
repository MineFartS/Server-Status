from ..Items import VirtualDisks, HardDrives, PCIeCards, Services, Towers, Mounts
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.time import sleep

def LogStatus(
    items: list
) -> None:
    
    for item in items:

        print(
            f'   {item.Name.ljust(35, '.')}: ',
            end = ''
        )

        if item.Connected:
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
    LogStatus(HardDrives)

    print('\nPCIe Cards:')
    LogStatus(PCIeCards)

    print('\nVirtual Disks:')
    LogStatus(VirtualDisks)

    print('\nMounts:')
    LogStatus(Mounts)

    print('\nTowers:')
    LogStatus(Towers)

    print('\nServices:')
    LogStatus(Services)

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, show=True)
