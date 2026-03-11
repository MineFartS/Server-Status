from ..Items import VirtualDisks, HardDrives, PCIeCards, Services, Towers
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.time import sleep

def LogStatus(
    title: str,
    items: list
) -> None:
    
    if len(items) > 0:

        print(f'\n{title}:')
    
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

    LogStatus('Hard Drives', HardDrives)

    LogStatus('PCIe Cards', PCIeCards)

    LogStatus('Virtual Disks', VirtualDisks)

    LogStatus('Towers', Towers)

    LogStatus('Services', Services)

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, show=True)
