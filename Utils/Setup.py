#=================================================================================
# PHILH_MYFTP_BIZ PKG

from . import Update # pyright: ignore[reportUnusedImport]

from ..Items import Modules

#=================================================================================
# Add Scheduled Tasks

Modules[0].run('xml/set', 'Startup')
Modules[0].run('xml/set', 'Hour')
Modules[0].run('xml/set', 'Week')

#=================================================================================
# INSTALL MODULES

for m in Modules:
    
    m.install()

#=================================================================================