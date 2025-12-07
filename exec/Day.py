from philh_myftp_biz.modules import Scanner
from __init__ import Plex

# Iter through all main modules
for mod in Scanner():

    # Install/Upgrade all dependencies
    mod.install()

    mod.git('add', '.')

    mod.git('commit', '-a', '-m', 'Automated Commit')

# Download 75 media items
Plex.run('torrenting/run')