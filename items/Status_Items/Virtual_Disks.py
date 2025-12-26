from philh_myftp_biz.process import RunHidden
from philh_myftp_biz.file import YAML
from . import this

# ===============================================================================================================

config = YAML(this.file('config/vDisks'))

# ===============================================================================================================

_raw: list[dict] = RunHidden(
    "Get-VirtualDisk -StoragePool (Get-StoragePool -FriendlyName 'Main Pool') | Select-Object FriendlyName, UniqueId, HealthStatus | ConvertTo-Json",
    terminal = 'ps'
).output('json')

if isinstance(_raw, dict):
    _raw = [_raw]

# ===============================================================================================================

class VirtualDisk:

    def __init__(self, name:str):
        
        self.Name = name
        self.UniqueID = None
        self.Connected = False

        for device in _raw:

            if device['FriendlyName'] == name:

                self.UniqueID: str = device['UniqueId']

                self.Connected = (device['HealthStatus'] != 'Unhealthy')

                break

# ===============================================================================================================

VirtualDisks: list[VirtualDisk] = []

for name in config.read():
    VirtualDisks += [VirtualDisk(name)]

# ===============================================================================================================
