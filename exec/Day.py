from __init__ import this
from philh_myftp_biz.modules import Scanner

# Backup Files
#this.run('run', 'backup', False)

# Iter through all main modules
for mod in Scanner():

    # Install/Upgrade all dependencies
    mod.install()