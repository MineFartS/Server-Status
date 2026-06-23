import os
os.add_dll_directory('C:/Scripts/lib/msys2/ucrt64/bin')
from main import HardDrive

hdd = HardDrive("HDD123")

print(f'{hdd.greet()=}')