from philh_myftp_biz.classtools import clear_cache
from philh_myftp_biz.process import RunHidden
from json.decoder import JSONDecodeError
from functools import cached_property
from dataclasses import dataclass
from typing import Literal

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
