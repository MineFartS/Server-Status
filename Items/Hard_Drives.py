from philh_myftp_biz.process import RunHidden
from functools import cache, cached_property
from philh_myftp_biz.terminal import Log
from typing import Literal

Log.VERB('Collecting Hard Drives')

# ===============================================================================================================
# PARSER

@cache
def physical_disks() -> list[dict]:
    return RunHidden(
        "Get-PhysicalDisk | ConvertTo-Json",
        terminal = 'ps'
    ).output(format='json') # pyright: ignore[reportReturnType]

@cache
def wmi_objects() -> list[dict]:
    return RunHidden(
        "Get-WmiObject Win32_DiskDrive | ConvertTo-Json",
        terminal = 'ps'
    ).output(format='json') # pyright: ignore[reportReturnType]

#==================================

class HardDrive:

    def __init__(self,
        tower: str,
        type: Literal['SATA', 'USB'],
        id: int,
        sn: str
    ) -> None:
        self.Tower = tower
        self.Type = type
        self.ID = id
        self.SerialNumber = sn
        self.Name = f'{str(id).zfill(2)}-{tower} [{type}]'

    @cached_property
    def _physical_disk(self) -> None | dict:

        for device in physical_disks():
            
            if device['SerialNumber'] == self.SerialNumber:

                return device
            
    @cached_property
    def _wmi_object(self) -> None | dict:

        for device in wmi_objects():
            
            if device['SerialNumber'] == self.SerialNumber:

                return device

    @cached_property
    def FriendlyName(self) -> None | str:
        
        if self._physical_disk:
            fname: str = self._physical_disk['FriendlyName']

            if len(fname) > 0:
                return fname

    @cached_property
    def UniqueID(self) -> None | str:
        if self._physical_disk:
            return self._physical_disk['UniqueId']
        
    @cached_property
    def Usage(self) -> None | Literal['Auto-Select', 'Retired']:
        if self._physical_disk:
            return self._physical_disk['Usage']

    @cached_property
    def Connected(self) -> bool:

        if self.FriendlyName:
            
            OpStatus: str = self._physical_disk['OperationalStatus']

            return (OpStatus != 'Lost Communication')
        
        else:
            return False
        
    @cached_property
    def RegPath(self) -> str | None:

        if self._wmi_object:

            pnpID: str = self._wmi_object['PNPDeviceID']

            return f"HKLM:SYSTEM\\ControlSet001\\Enum\\{pnpID}"

# ===============================================================================================================
# CONFIGURATION

HardDrives: list[HardDrive] = [

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

    HardDrive(
        tower = 'A',
        type = 'SATA',
        id = 3,
        sn = None
    ),

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

    HardDrive(
        tower = 'B',
        type = 'SATA',
        id = 11,
        sn = '01CB9083B07Z'
    ),

    HardDrive(
        tower = 'C',
        type = 'SATA',
        id = 12,
        sn = 'Z992XWLF'
    ),

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