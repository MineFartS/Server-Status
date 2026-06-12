from philh_myftp_biz.classtools import clear_cache
from functools import cached_property
from dataclasses import dataclass

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
