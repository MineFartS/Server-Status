from philh_myftp_biz.modules import Service as __Service
from philh_myftp_biz.classtools import clear_cache
from philh_myftp_biz.process import RunHidden
from json.decoder import JSONDecodeError
from functools import cached_property
from typing import Literal, Generator
from philh_myftp_biz.pc import Path
from dataclasses import dataclass

class Service(__Service):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.running

class Mount(Path):

    @cached_property
    def Name(self) -> str:
        return self.path

    @property
    def Connected(self) -> bool:
        return self.exists

@dataclass
class VirtualDisk:

    Name: str

    @cached_property
    def UniqueID(self) -> None | str:

        if self._virtual_disk:
            
            return self._virtual_disk['UniqueId']

    @cached_property
    def Connected(self) -> bool:

        if self._virtual_disk:

            healthStatus: str = self._virtual_disk['HealthStatus']

            return (healthStatus != 'Unhealthy')
        
        else:
            return False

    @cached_property
    def _virtual_disk(self) -> None | dict:
        try:
        
            return RunHidden(
                f"Get-VirtualDisk -FriendlyName {self.Name} | ConvertTo-Json",
                terminal = 'ps'
            ).output(format='json') # pyright: ignore[reportReturnType]
        
        except JSONDecodeError:
            pass

    def repair(self) -> None:
        RunHidden(
            f"Repair-VirtualDisk -UniqueId '{self.UniqueID}'",
            terminal = 'ps'
        )

    #================
    # Usage

    @property
    def Mounted(self) -> bool:
        
        if self._virtual_disk:

            DetachedReason: str = self._virtual_disk['DetachedReason']
            
            return (DetachedReason == 'None')
        
        else:

            return False
        
    @Mounted.setter
    def Mounted(self,
        mounted: bool
    ) -> None:
        
        if self.Mounted != mounted:

            if mounted:
                cmd = 'Connect'
            else:
                cmd = 'Disconnect'

            RunHidden(
                f"{cmd}-VirtualDisk -UniqueId '{self.UniqueID}'",
                terminal = 'ps'
            )

    #================

@dataclass
class HardDrive:

    Tower: str
    Conn: Literal['SATA', 'USB']
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
    def HardDrives(self) -> Generator[HardDrive]:
        from . import HardDrives

        for hdd in HardDrives:
        
            if hdd.Tower == self.ID:

                yield hdd

    @property
    def Connected(self) -> bool:

        clear_cache(self)

        return any(hdd.Connected for hdd in self.HardDrives)
