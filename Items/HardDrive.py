from json.decoder import JSONDecodeError
from dataclasses import dataclass
from typing import Literal, Any

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
        try:
            return self._cpp('Connected') # pyright: ignore[reportReturnType]
        except JSONDecodeError:
            return False

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
