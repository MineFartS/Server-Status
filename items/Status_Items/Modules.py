from philh_myftp_biz.modules import Module
from philh_myftp_biz.file import YAML
from . import this

# ===============================================================================================================

config = YAML(this.file('config/modules')).read()

# ===============================================================================================================

Modules: dict[str, Module] = {}

for m in config:

    try:
        Modules[m.lower()] = Module(config[m])
        
    except ModuleNotFoundError:
        pass

# ===============================================================================================================
