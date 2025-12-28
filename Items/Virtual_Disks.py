from philh_myftp_biz.process import RunHidden

# ===============================================================================================================

_raw: list[dict] = RunHidden(
    "Get-VirtualDisk | Select-Object FriendlyName, UniqueId, HealthStatus | ConvertTo-Json",
    terminal = 'ps'
).output('json')

if isinstance(_raw, dict):
    _raw = [_raw]

# ===============================================================================================================

class VirtualDisk:

    def __init__(self, rDisk:dict):
        
        self.Name = rDisk['FriendlyName']
        self.UniqueID = rDisk['UniqueId']
        self.Connected = (rDisk['HealthStatus'] != 'Unhealthy')

# ===============================================================================================================

VirtualDisks: list[VirtualDisk] = []

for rDisk in _raw:

    VirtualDisks += [VirtualDisk(rDisk)]

# ===============================================================================================================
