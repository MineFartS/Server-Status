from __init__ import mnt
from philh_myftp_biz import run
from philh_myftp_biz.pc import pause, cls

cls()

# Delete lock file
lockfile = mnt.E.child('.git/index.lock')
if lockfile.exists():
    lockfile.delete()

# Add all of the files 
run(
    args = ['git', 'add', '.', '-v'],
    wait = True,
    dir = mnt.E
)

# Commit
run(
    args = ['git', 'commit', '-m', 'Automatic Commit'],
    wait = True,
    dir = mnt.E
)

pause()