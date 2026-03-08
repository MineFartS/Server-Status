from philh_myftp_biz.process import RunHidden
from functools import cache, cached_property
from philh_myftp_biz.terminal import Log
from typing import Literal

Log.VERB('Collecting PCIe Cards')

# ===============================================================================================================
# PARSER

@cache
def pnp_devices() -> list[dict]:
    return RunHidden(
        "Get-PnpDevice | Where-Object InstanceId -like 'PCI\\*' | Select-Object DeviceId, Status | ConvertTo-Json",
        terminal = 'ps'
    ).output('json') # pyright: ignore[reportReturnType]

class PCIeCard:

    def __init__(self,
        slot: Literal[1, 2, 3, 4, 'M.2'],
        lanes: Literal[1, 4, 16],
        id: str
    ) -> None:
        
        if isinstance(slot, int):
            self.Name = f'Slot {str(slot)} [x{str(lanes)}]'

        elif isinstance(slot, str):
            self.Name = f'{slot} [x{str(lanes)}]'

        self.Lanes: int = lanes
        
        self.DeviceID: str = id

    @cached_property
    def _pnp_device(self) -> None | dict:

        for device in pnp_devices():
            
            if device['DeviceId'] == self.DeviceID:

                return device

    @cached_property
    def Connected(self) -> bool:

        if self._pnp_device:
            return (self._pnp_device['Status'] == 'OK')
        
        else:
            return False

# ===============================================================================================================
# CONFIGURATION

PCIeCards = [

    PCIeCard(
        slot = 1,
        lanes = 1,
        id = "PCI\\VEN_1B21&DEV_2142&SUBSYS_21421B21&REV_00\\4&33FC7E38&0&00E0"
    ),

    PCIeCard(
        slot = 2,
        lanes = 16,
        id = "PCI\\VEN_10DE&DEV_13BA&SUBSYS_109710DE&REV_A2\\4&787313E&0&0008"
    ),

    PCIeCard(
        slot = 3,
        lanes = 4,
        id = "PCI\\VEN_1B21&DEV_1064&SUBSYS_21161B21&REV_02\\4&F6FAD87&0&00E8"
    ),

    PCIeCard(
        slot = 'M.2',
        lanes = 4,
        id = "PCI\\VEN_1B21&DEV_1166&SUBSYS_21162116&REV_02\\4&1E804E93&0&00D8"
    )

]

# ===============================================================================================================