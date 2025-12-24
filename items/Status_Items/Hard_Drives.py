from philh_myftp_biz.file import YAML
from philh_myftp_biz import run
from typing import Literal
from . import this

# ===============================================================================================================

config = YAML(this.file('config/Hard Drives'))

# ===============================================================================================================

_raw: list[dict] = run(
    "Get-PhysicalDisk | Select-Object SerialNumber, FriendlyName, OperationalStatus, UniqueId, Usage | ConvertTo-Json",
    wait = True,
    terminal = 'ps',
    hide = True
).output('json')

# ===============================================================================================================

class HardDrive:

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

        for device in _raw:
            if device['SerialNumber'] == sn:

                self.FriendlyName: str = device['FriendlyName']
                self.UniqueID: str = device['UniqueId']
                self.Usage: str = device['Usage']
                
                if len(self.FriendlyName) > 0:
                    self.Connected: bool = (device['OperationalStatus'] != 'Lost Communication')

                break

# ===============================================================================================================

HardDrives: list['HardDrive'] = []

for tower, type, id, sn in config.read():
    HardDrives += [HardDrive(tower, type, id, sn)]

# ===============================================================================================================