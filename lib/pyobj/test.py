import os
os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')
from main import HardDrive

hdd = HardDrive("UGXVK01J7BANIX")

print(f'{hdd.Connected=}')

print(f'{hdd.FriendlyName=}')

print(f'{hdd.Usage=}')
