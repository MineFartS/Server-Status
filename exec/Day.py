from philh_myftp_biz.modules import Scanner

# ==================================================

# Iter through all main modules
for mod in Scanner():

    # Install/Upgrade all dependencies
    mod.install()

    mod.git('add', '.')

    mod.git('commit', '-a', '-m', 'Automated Commit')

# ==================================================
