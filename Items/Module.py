from philh_myftp_biz.modules import Module as __Module
from functools import cached_property

class Module(__Module):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.exists


