from philh_myftp_biz.modules import Service
from philh_myftp_biz.file import YAML
from .Modules import Modules
from . import this

# ===============================================================================================================

config = YAML(this.file('config/services'))

# ===============================================================================================================

Services: list[Service] = []

for m, p in config.read():
 
    try:
        Services += [Service(    
            module = Modules[m.lower()],
            path = p
        )]
        
    except KeyError:
        pass

# ===============================================================================================================
