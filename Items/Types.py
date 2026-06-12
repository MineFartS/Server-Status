from philh_myftp_biz.modules import Service as __Service
from philh_myftp_biz.modules import Module as __Module
from functools import cached_property

from . import VirtualDisk, HardDrive, PCIeCard, Tower # pyright: ignore[reportUnusedImport]

class Service(__Service):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.running

class Module(__Module):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.exists


