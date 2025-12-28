from subprocess import run
from sys import executable

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

from .Items.Modules import Modules

for m in Modules:
    
    m.install()
