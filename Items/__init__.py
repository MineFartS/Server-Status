from .Types import HardDrive, PCIeCard, Service, Tower, VirtualDisk
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import NAME
from importlib import import_module

print(f'{NAME().replace('-', '')=}')

def getItems(file:str) -> list:    

    Log.VERB(f'Collecting Items: {file}')

    dirname = NAME().replace('-', '')

    try:
    
        return import_module(
            name = f'.{dirname}.{file}', 
            package = __name__
        ).Items
    
    except ModuleNotFoundError:
        return []

HardDrives: list[HardDrive] = getItems('HardDrives')

Modules: list[Module] = getItems('Modules')

PCIeCards: list[PCIeCard] = getItems('PCIeCards')

Services: list[Service] = getItems('Services')

Towers: list[Tower] = getItems('Towers')

VirtualDisks: list[VirtualDisk] = getItems('VirtualDisks')
