from .Types import HardDrive, PCIeCard, Service, Tower, VirtualDisk, Mount
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import NAME
from importlib import import_module

def getItems(file:str):    

    Log.VERB(f'Collecting Items: {file}')

    dirname = NAME().replace('-', '')

    return import_module(
        name = f'.{dirname}.{file}', 
        package = __name__
    ).Items

HardDrives: list[HardDrive] = getItems('HardDrives')

Modules: list[Module] = getItems('Modules')

PCIeCards: list[PCIeCard] = getItems('PCIeCards')

Services: list[Service] = getItems('Services')

Towers: list[Tower] = getItems('Towers')

VirtualDisks: list[VirtualDisk] = getItems('VirtualDisks')

Mounts: list[Mount] = getItems('Mounts')
