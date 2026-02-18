from subprocess import run
from sys import executable

#=================================================================================
# PHILH_MYFTP_BIZ PKG

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

#=================================================================================
# SYNCORD

# Install requirements
run(
    args = [executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
    cwd = 'C:/Scripts/exec/syncord'
)

# Update Token
run(
    args = [
        executable, 'main.py', 'setup',
        '--token', 'MTQ3MzcxMzM3MTIzMTU1MTYzOQ.GT6kTr.mQ-YAKlb3jh5jQsjM2cxuG9s3M6kIkcIwcqsDc', # Bot Token
        '--guild-id', '1440308657706242154' # Discord Server ID
    ],
    cwd = 'C:/Scripts/exec/syncord'
)

#=================================================================================
# MODULES

from .Items.Modules import Modules

for m in Modules:
    
    m.install()

#=================================================================================