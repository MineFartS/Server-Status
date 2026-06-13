from philh_myftp_biz.modules import Service as __Service
from functools import cached_property

class Service(__Service):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.running

