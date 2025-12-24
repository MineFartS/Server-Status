from philh_myftp_biz.modules import Service, Module
from philh_myftp_biz.file import YAML
from . import this

# ===============================================================================================================

config = YAML(this.file('config/services'))

# ===============================================================================================================

Services: list[Service] = []

for paths in config.read():

    try:
        
        Services += [Service(
            
            module = Module(paths[0]),
        
            path = paths[1]
        
        )]
        
    except ModuleNotFoundError:
        pass    

# ===============================================================================================================
