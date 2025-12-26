from .Modules import Modules

# ==================================================

# Iter through all main modules
for mod in Modules:

    # Install/Upgrade all dependencies
    mod.install()

    mod.git('add', '.')

    mod.git('commit', '-a', '-m', 'Automated Commit')

# ==================================================
