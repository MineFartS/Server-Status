from subprocess import run
from sys import executable

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

from philh_myftp_biz.modules import Scanner
from philh_myftp_biz.pc import Path

for m in Scanner():
    
    m.install(hide=False)
