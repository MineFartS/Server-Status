from philh_myftp_biz.process import RunHidden
from functools import cache, cached_property
from philh_myftp_biz.terminal import Log

Log.VERB('Collecting Virtual Disks')

# ===============================================================================================================

@cache
def virtual_disks() -> list[dict]:

    data: dict | list[dict] = RunHidden(
        "Get-VirtualDisk | Select-Object FriendlyName, UniqueId, HealthStatus | ConvertTo-Json",
        terminal = 'ps'
    ).output('json')

    if isinstance(data, dict):
        return [data]
    else:
        return data

# ===============================================================================================================

class VirtualDisk:

    def __init__(self,
        name: str
    ) -> None:
        self.Name = name

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

        for device in virtual_disks():

            if device['FriendlyName'].lower() == self.Name.lower():

                return device

# ===============================================================================================================

VirtualDisks: list[VirtualDisk] = [

    VirtualDisk('Main Disk'),

    VirtualDisk('Plex Media')

]

# ===============================================================================================================
