from subprocess import run
from sys import executable
from .Items import Modules

#=================================================================================
# PHILH_MYFTP_BIZ PKG

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

#=================================================================================
# INSTALL MODULES

for m in Modules:
    
    m.install()

#=================================================================================