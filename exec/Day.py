from philh_myftp_biz.modules import Scanner
from __init__ import Plex

# Iter through all main modules
for mod in Scanner():

    # Install/Upgrade all dependencies
    mod.install()

    mod.git('add', '.')

    mod.git('commit', '-a', '-m', 'Automated Commit')

# Download 15 items to plex
Plex.run('torrenting/run', '--limit', '15')