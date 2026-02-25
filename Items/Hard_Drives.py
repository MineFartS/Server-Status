
# ===============================================================================================================
# PARSER

from philh_myftp_biz.process import RunHidden
from typing import Literal

physical_disks: list[dict] = RunHidden(
    "Get-PhysicalDisk | ConvertTo-Json",
    terminal = 'ps'
).output('json')

wmi_objects: list[dict] = RunHidden(
    "Get-WmiObject Win32_DiskDrive | ConvertTo-Json",
    terminal = 'ps'
).output('json')

class HardDrive:

    FriendlyName: str = None
    
    UniqueID: str = None
    
    Usage: Literal['Auto-Select', 'Retired'] = None 
    
    RegPath: str = None
    
    Connected: bool = False

    def __init__(self,
        tower: str,
        type: Literal['SATA', 'USB'],
        id: int,
        sn: str
    ):
        
        self.Tower = tower
        self.Type = type
        self.ID = id
        self.SerialNumber = sn
        self.Name = f'{str(id).zfill(2)}-{tower} [{type}]'

        for device in physical_disks:
            
            if device['SerialNumber'] == sn:

                self.FriendlyName: str = device['FriendlyName']
                self.UniqueID    : str = device['UniqueId']
                self.Usage       : str = device['Usage']
                
                if len(self.FriendlyName) > 0:
                    self.Connected: bool = (device['OperationalStatus'] != 'Lost Communication')

                break

        for device in wmi_objects:

            if device['SerialNumber'] == sn:

                self.RegPath: str = f"HKLM:SYSTEM\\ControlSet001\\Enum\\" + device['PNPDeviceID'] 

                break

# ===============================================================================================================
# CONFIGURATION

HardDrives = [

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 1,
        sn = 'PBEHHBB250616011613'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 2,
        sn = '0000DHM1'
    ),

    #HardDrive(
    #    tower = 'A',
    #    type = 'SATA',
    #    id = 3,
    #    sn = None
    #),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 4,
        sn = 'YHHPB2LA'
    ),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 5,
        sn = 'YHKK76GG'
    ),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 6,
        sn = 'YHKPSRSA'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 7,
        sn = '134605400828'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 8,
        sn = 'YXGLGSXG'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 9,
        sn = 'S3TCNC0M500604'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 10,
        sn = 'QNVZGLRX'
    ),

    #HardDrive(
    #    tower = 'B',
    #    type = 'SATA',
    #    id = 11,
    #    sn = '01CB9083B07Z'
    #),

    #HardDrive(
    #    tower = 'C',
    #    type = 'SATA',
    #    id = 12,
    #    sn = 'Z992XWLF'
    #),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 13,
        sn = 'V8H6T9ZR'
    ),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 14,
        sn = 'YVJ42ZAA'
    ),

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 15,
        sn = 'UGXVK01J7BANIX'
    ),

    HardDrive(
        tower = 'B',
        type = 'SATA',
        id = 16,
        sn = 'ZR11FS39'
    ),

    HardDrive(
        tower = 'B',
        type = 'SATA',
        id = 17,
        sn = 'ZGY43H7A'
    ),

    HardDrive(
        tower = 'B',
        type = 'SATA',
        id = 18,
        sn = 'Z5M3K0R6FUUB'
    ),

    HardDrive(
        tower = 'B',
        type = 'SATA',
        id = 19,
        sn = 'Z5H1K13BFUUB'
    )

]

# ===============================================================================================================