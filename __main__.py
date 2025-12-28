from os import system
from sys import argv

# Clear the terminal window
system('cls')

# Relatively execute the script via import
exec(f'from .{argv[1]} import *')
