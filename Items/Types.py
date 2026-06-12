from philh_myftp_biz.modules import Service as __Service
from philh_myftp_biz.modules import Module as __Module
from philh_myftp_biz.classtools import clear_cache
from philh_myftp_biz.process import RunHidden, Run
from json.decoder import JSONDecodeError
from functools import cached_property
from philh_myftp_biz.pc import Path
from dataclasses import dataclass
from typing import Literal, Any

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

    def _cpp(self, *args:str) -> dict[str, Any]:
        from . import Modules
        
        return Modules[0].runH(
            'lib/diskutils/run', self.SN, *args
        ).output('json')['result'] # pyright: ignore[reportReturnType]

    #================
    # Name

    @property
    def Name(self) -> str:
        return f'{self.ID:02d}-{self.Tower} [{self.Conn}]'

    #================
    # Connected

    @property
    def Connected(self) -> bool:
        return self._cpp('Connected') # pyright: ignore[reportReturnType]

    #================
    # FriendlyName

    @property
    def FriendlyName(self) -> None | str:
        return self._cpp('FriendlyName') # pyright: ignore[reportReturnType]

    @FriendlyName.setter
    def FriendlyName(self, name:str) -> None:
        self._cpp('FriendlyName', name)

    #================
    # Usage

    @property
    def Usage(self) -> None | Literal['Auto-Select', 'Retired']:
        return self._cpp('Usage') # pyright: ignore[reportReturnType]
        
    @Usage.setter
    def Usage(self,
        usage: Literal['Auto-Select', 'Retired']
    ) -> None:
        self._cpp('Usage', usage)

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
