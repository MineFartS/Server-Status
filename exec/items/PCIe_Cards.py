from philh_myftp_biz.file import YAML
from philh_myftp_biz import run
from typing import Literal
from __init__ import this

# ===============================================================================================================

config = YAML(this.file('config/PCIe Cards'))

# ===============================================================================================================

_raw: list[dict] = run(
    "Get-PnpDevice | Where-Object InstanceId -like 'PCI\\*' | Select-Object DeviceId, Status | ConvertTo-Json",
    wait = True,
    terminal = 'ps',
    hide = True
).output('json')

# ===============================================================================================================

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

PCIeCards: list['PCIeCard'] = []

for slot, lanes, id in config.read():
    
    PCIeCards += [PCIeCard(
        slot = slot,
        lanes = lanes,
        id = id
    )]

# ===============================================================================================================