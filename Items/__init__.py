from subprocess import run

run(['Powershell.exe', '-File', 'C:/Scripts/lib/pyobj/build.ps1'])

from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import NAME
from importlib import import_module

import os
os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')

from ._cpp import HardDrive, PCIeCard, VirtualDisk

from .Service import Service
from .Tower import Tower

def getItems(file:str) -> list:    

    Log.VERB(f'Collecting Items: {file}')

    dirname = NAME.replace('-', '')

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
