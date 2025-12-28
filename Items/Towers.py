
# ===============================================================================================================
# PARSER

from .Hard_Drives import HardDrives

class Tower:

    def __init__(self, id:str):

        self.ID = id

        self.Name = f'Tower {id}'

        self.Connected: bool = False

        for hdd in HardDrives:
        
            if (hdd.Tower == id) and hdd.Connected:

                self.Connected = True

                break
        
# ===============================================================================================================
# CONFIGURATION

Towers: list[Tower] = [

    Tower('A'),

    Tower('B'),

    Tower('C')

]

# ===============================================================================================================