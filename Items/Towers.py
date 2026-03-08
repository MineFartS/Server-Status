from .Hard_Drives import HardDrives, HardDrive
from philh_myftp_biz.terminal import Log
from functools import cached_property
from typing import Generator

Log.VERB('Collecting Towers')

# ===============================================================================================================
# PARSER

class Tower:

    def __init__(self, id:str):

        self.ID = id

        self.Name = f'Tower {id}'

    @cached_property
    def HardDrives(self) -> Generator[HardDrive]:

        for hdd in HardDrives:
        
            if hdd.Tower == self.ID:

                yield hdd

    @cached_property
    def Connected(self) -> bool:

        return any(hdd.Connected for hdd in self.HardDrives)
        
# ===============================================================================================================
# CONFIGURATION

Towers: list[Tower] = [

    Tower('A'),

    Tower('B'),

    Tower('C')

]

# ===============================================================================================================