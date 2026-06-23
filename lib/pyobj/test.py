import os
os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')
from main import HardDrive

hdd = HardDrive(
    Tower = 'A',
    Conn = 'SATA',
    ID = 1,
    SN = 'PBEHHBB250616011613'
)

print(f'{hdd.Connected=}')

print(f'{hdd.Tower=}')

print(f'{hdd.Conn=}')

print(f'{hdd.ID=}')

print(f'{hdd.Name=}')

print(f'{hdd.FriendlyName=}')

print(f'{hdd.Usage=}')