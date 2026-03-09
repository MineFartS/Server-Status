from ..Items import Modules

#=================================================================================
# PHILH_MYFTP_BIZ PKG

from . import Update # pyright: ignore[reportUnusedImport]

#=================================================================================
# INSTALL MODULES

for m in Modules:
    
    m.install()

#=================================================================================