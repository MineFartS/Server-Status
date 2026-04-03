from philh_myftp_biz.web import FirewallException as __FirewallException
from philh_myftp_biz.modules import Service as __Service
from philh_myftp_biz.modules import Module as __Module
from philh_myftp_biz.classtools import clear_cache
from philh_myftp_biz.process import RunHidden, Run
from json.decoder import JSONDecodeError
from functools import cached_property
from philh_myftp_biz.pc import Path
from dataclasses import dataclass
from typing import Literal

class Service(__Service):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.running

class Module(__Module):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.exists

@dataclass
class VirtualDisk:

    Name: str
    Mount: Path

    @property
    def Connected(self) -> bool:
        return self.Mount.exists

    def _ps(self, cmd:str):        
        Run(
            f"{cmd}-VirtualDisk -FriendlyName '{self.Name}'",
            terminal = 'ps'
        )

    @Connected.setter
    def Connected(self, connect:bool) -> None:
        
        if connect:

            # Connect-VirtualDisk
            self._ps('Connect')

            # Repair-VirtualDisk
            self._ps('Repair')

        else:

            # Disconnect-VirtualDisk
            self._ps('Disconnect')

@dataclass
class HardDrive:

    Tower: str
    Conn: Literal['SATA', 'USB', 'PROP']
    ID: int
    SN: str

    @cached_property
    def Name(self) -> str:
        return f'{self.ID:02d}-{self.Tower} [{self.Conn}]'

    @cached_property
    def _physical_disk(self) -> None | dict:
        try:

            return RunHidden(
                f"Get-PhysicalDisk -SerialNumber {self.SN} | ConvertTo-Json",
                terminal = 'ps'
            ).output(format='json') # pyright: ignore[reportReturnType]
        
        except JSONDecodeError:
            pass
            
    @cached_property
    def _wmi_object(self) -> None | dict:
        try:

            return RunHidden(
                [
                    'Get-WmiObject', '-Query', 
                    f"SELECT * FROM Win32_DiskDrive WHERE SerialNumber = '{self.SN}'",
                    '| ConvertTo-Json'
                ],
                terminal = 'ps'
            ).output(format='json') # pyright: ignore[reportReturnType]
        
        except JSONDecodeError:
            pass

    @cached_property
    def UniqueID(self) -> None | str:

        if self._physical_disk:
        
            return self._physical_disk['UniqueId']
        
    @property
    def Connected(self) -> bool:

        clear_cache(self)

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

    #================
    # FriendlyName

    @property
    def FriendlyName(self) -> None | str:
        
        if self._physical_disk:

            FriendlyName: str = self._physical_disk['FriendlyName']

            if len(FriendlyName) > 0:
                
                return FriendlyName

    @FriendlyName.setter
    def FriendlyName(self,
        name: str
    ) -> None:
        
        if name != self.FriendlyName:
        
            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{self.UniqueID}' -NewFriendlyName '{name}'",
                terminal = 'ps'
            )

            # If disk has a registry path 
            if self.RegPath:

                # Update the Friendly Name in the windows registry
                RunHidden(
                    f"Set-ItemProperty '{self.RegPath}' FriendlyName '{self.Name}'",
                    terminal = 'ps'
                )

            clear_cache(self)

    #================
    # Usage

    @property
    def Usage(self) -> None | Literal['Auto-Select', 'Retired']:
        
        if self._physical_disk:
            
            return self._physical_disk['Usage']
        
    @Usage.setter
    def Usage(self,
        usage: Literal['Auto-Select', 'Retired']
    ) -> None:
        
        if usage != self.Usage:

            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{self.UniqueID}' -Usage {usage}",
                terminal = 'ps'
            )

            clear_cache(self)

    #================

@dataclass
class PCIeCard:

    Slot: Literal[1, 2, 3, 4, 'M.2']
    Lanes: Literal[1, 4, 16]
    DeviceID: str

    @cached_property
    def Name(self) -> str:
        
        if isinstance(self.Slot, int):
            return f'Slot {self.Slot} [x{self.Lanes}]'

        else:
            return f'{self.Slot} [x{self.Lanes}]'

    @cached_property
    def _pnp_device(self) -> None | dict:
        try:

            return RunHidden(
                f"Get-PnpDevice -DeviceId '{self.DeviceID}' | ConvertTo-Json",
                terminal = 'ps'
            ).output(format='json') # pyright: ignore[reportReturnType]
        
        except JSONDecodeError:
            pass

    @property
    def Connected(self) -> bool:

        clear_cache(self)

        if self._pnp_device:
            return (self._pnp_device['Status'] == 'OK')
        
        else:
            return False

@dataclass
class Tower:

    ID: str

    @cached_property
    def Name(self) -> str:
        return f'Tower {self.ID}'

    @cached_property
    def Connected(self) -> bool:
        from . import HardDrives

        clear_cache(self)

        _HardDrives = filter(
            lambda hdd: (hdd.Tower == self.ID),
            HardDrives
        )

        _HardDrives = filter(
            lambda hdd: hdd.Connected,
            _HardDrives
        )

        return next(_HardDrives, None) != None

class FWPort(__FirewallException):

    def __init__(self,
        name: str,
        port: int
    ) -> None:

        super().__init__(name)

        self.Name = name

        self._port = port

    def set(self):
        super().set(self._port)

    @property
    def Connected(self):
        return self.exists
