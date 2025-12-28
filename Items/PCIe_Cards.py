# ===============================================================================================================
# PARSER

from philh_myftp_biz.process import RunHidden
from typing import Literal

_raw: list[dict] = RunHidden(
    "Get-PnpDevice | Where-Object InstanceId -like 'PCI\\*' | Select-Object DeviceId, Status | ConvertTo-Json",
    terminal = 'ps'
).output('json')

class PCIeCard:

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

        for device in _raw:
            if device['DeviceId'] == id:

                self.Connected: bool = (device['Status'] == 'OK')

                break

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