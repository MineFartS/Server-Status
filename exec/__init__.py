from philh_myftp_biz.web import online, get, WiFi
from philh_myftp_biz.pc import Path, script_dir
from philh_myftp_biz.modules import Module
from philh_myftp_biz.file import YAML
from philh_myftp_biz import run
from typing import Literal

# ===============================================================================================================

this = Module(script_dir(__file__).parent())

try:
    AI = Module('E:/AI')
    Web = Module('E:/Website')
    Plex = Module('E:/Plex')
except ModuleNotFoundError:
    AI = None
    Web = None
    Plex = None

options = YAML(this.file('config/options')).read()

class mnt:
    C = Path('C:/')
    E = Path('E:/')
    D = Path('D:/')

wifi = WiFi()

# ===============================================================================================================

def alert(m):

    if online() and options['alert']['sms']:
        # Send SMS Alert
        get(
            url = 'https://script.google.com/macros/s/AKfycbztUPSGrf9lnl3_qIBjBui6pDSl_errjxdEi_9LnGNO0TjgMeZDBvWvrQBU36P80x0/exec',
            params = {'message' : m}
        )

    if options['alert']['popup']:
        # Show Alert Box
        this.start('exec/alert', m)

def LogStatus(name:str, connected:bool):
    from philh_myftp_biz.pc import print

    print(
        '   {} : '.format(name.ljust(12, ' ')),
        end = ''
    )

    if connected:
        print(
            'Connected',
            color = 'GREEN'
        )
    else:
        print(
            'Missing',
            color = 'RED'
        )

# ===============================================================================================================

class devices:

    # ===============================================================================================================
    # HARD DRIVES

    class HardDrive:

        __PS_Data: list[dict] = run(
            "Get-PhysicalDisk | Select-Object SerialNumber, FriendlyName, OperationalStatus, UniqueId, Usage | ConvertTo-Json",
            wait = True,
            terminal = 'ps',
            hide = True
        ).output('json')

        def __init__(self,
            tower: Literal['A', 'B', 'C', 'EXT'],
            type: Literal['SATA', 'USB'],
            id: int,
            sn: str
        ):
            
            self.Tower = tower
            self.Type = type
            self.ID = id
            self.SerialNumber = sn
            self.Name = f'{str(id).zfill(2)}-{tower} [{type}]'

            self.FriendlyName = None
            self.UniqueID = None
            self.Usage = None 
            self.Connected = False

            for device in self.__PS_Data:
                if device['SerialNumber'] == sn:

                    self.FriendlyName: str = device['FriendlyName']
                    self.UniqueID: str = device['UniqueId']
                    self.Usage: str = device['Usage']
                    
                    if len(self.FriendlyName) > 0:
                        self.Connected: bool = (device['OperationalStatus'] != 'Lost Communication')

                    break

    HardDrives: list['HardDrive'] = []

    for tower, type, id, sn in YAML(this.file('config/Hard Drives')).read():
        HardDrives += [HardDrive(tower, type, id, sn)]

    # ===============================================================================================================
    # PCIE CARDS

    class PCIeCard:

        __PS_Data: list[dict] = run(
            "Get-PnpDevice | Where-Object InstanceId -like 'PCI\\*' | Select-Object DeviceId, Status | ConvertTo-Json",
            wait = True,
            terminal = 'ps',
            hide = True
        ).output('json')

        def __init__(self,
            slot: Literal[1, 2, 3, 4, 'M.2'],
            lanes: Literal[1, 4, 16],
            id: str
        ):
            
            if isinstance(slot, int):
                self.Name = f'Slot {str(slot)} [x{str(lanes)}]'
            elif isinstance(slot, str):
                self.Name = f'{slot} [x{str(lanes)}]'

            self.Lanes = lanes
            self.DeviceID = id
            self.Connected = False

            for device in self.__PS_Data:
                if device['DeviceId'] == id:

                    self.Connected: bool = (device['Status'] == 'OK')

                    break
    
    PCIeCards: list['PCIeCard'] = []

    for slot, lanes, id in YAML(this.file('config/PCIe Cards')).read():
        PCIeCards += [PCIeCard(
            slot = slot,
            lanes = lanes,
            id = id
        )]

    # ===============================================================================================================
    # VIRTUAL DISKS

    class VirtualDisk:

        __PS_Data: list[dict] = run(
            "Get-VirtualDisk -StoragePool (Get-StoragePool -FriendlyName 'Main Pool') | Select-Object FriendlyName, UniqueId, HealthStatus | ConvertTo-Json",
            wait = True,
            terminal = 'ps',
            hide = True
        ).output('json')

        if isinstance(__PS_Data, dict):
            __PS_Data = [__PS_Data]

        def __init__(self, name:str):
            
            self.Name = name
            self.UniqueID = None
            self.Connected = False

            for device in self.__PS_Data:

                if device['FriendlyName'] == name:

                    self.Connected = (device['HealthStatus'] != 'Unhealthy')

                    break

    VirtualDisks: list[VirtualDisk] = []

    for name in YAML(this.file('config/vDisks')).read():
        VirtualDisks += [VirtualDisk(name)]

    # ===============================================================================================================
    # TOWERS

    class Tower:

        def __init__(self, id:str, connected:bool):

            self.ID = id

            self.Name = f'Tower {id}'

            self.Connected = connected
            
    Towers: list[Tower] = []

    for id in ['A', 'B', 'C']:

        for hdd in HardDrives:
            
            if (hdd.Tower == id) and hdd.Connected:
                
                Towers += [Tower(id, True)]

                break

        # If no connected hard drives are found for the tower
        else:

            # Append the tower
            Towers += [Tower(id, False)]

    # ===============================================================================================================

# ===============================================================================================================