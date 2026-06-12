from philh_myftp_biz.process import Run
from philh_myftp_biz.pc import Path
from dataclasses import dataclass

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
