#==========================================================
from pybind11_stubgen import main
from subprocess import run
import os, sys

os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')

run(['Powershell.exe', '-File', 'C:/Scripts/lib/pyobj/build.ps1', '-v'])

sys.path.append('C:/Scripts/Items/')
if not os.path.exists('C:/Scripts/Items/_cpp.pyi'):
    main(['_cpp', '--output-dir', 'C:/Scripts/Items/'])

if '_cpp' in sys.modules:
    sys.modules[f"{__name__}._cpp"] = sys.modules['_cpp']

#==========================================================
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import NAME
from importlib import import_module

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

#==========================================================

