from subprocess import run
import os, sys

#==========================================================
# BUILD

os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')

run(['Powershell.exe', '-File', 'C:/Scripts/lib/pyobj/build.ps1', '-v'])

#==========================================================
# STUBGEN

if not os.path.exists('C:/Scripts/Items/_cpp.pyi'):
    
    sys.path.append('C:/Scripts/Items/')
    
    run([sys.executable, '-m', 'pip', 'install', 'pybind11-stubgen'])
    from pybind11_stubgen import main

    main(['_cpp', '--output-dir', 'C:/Scripts/Items/'])

if '_cpp' in sys.modules:
    sys.modules[f"{__name__}._cpp"] = sys.modules['_cpp']

#==========================================================
# SCAN ITEMS

from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import NAME, Path
from philh_myftp_biz.terminal import Log
from importlib import import_module
from wmi import WMI

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

#=============

HardDrives: list[HardDrive] = getItems('HardDrives')

for disk in WMI().Win32_DiskDrive():

    sn: str = disk.SerialNumber.strip()

    if not any ([ 
        sn.startswith('{'),
        *((i.SN == sn) for i in HardDrives)
    ]):
        HardDrives += [HardDrive(
            Tower = '?',
            Conn = '?',
            ID = 0,
            SN = sn
        )]

#=============

Services: list[Service] = getItems('Services')

Services += [Service(d) for d in Path('C:/Scripts/Services/').children if d.is_dir]

#=============

Modules: list[Module] = getItems('Modules')

PCIeCards: list[PCIeCard] = getItems('PCIeCards')

Towers: list[Tower] = getItems('Towers')

VirtualDisks: list[VirtualDisk] = getItems('VirtualDisks')

#==========================================================

