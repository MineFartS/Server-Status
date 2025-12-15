from subprocess import run
from sys import executable

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

from philh_myftp_biz.modules import Scanner

for m in Scanner():
    
    m.install(hide=False)
