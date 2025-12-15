from philh_myftp_biz.modules import Service, Module
from philh_myftp_biz.file import YAML
from __init__ import this

# ===============================================================================================================

config = YAML(this.file('config/services'))

# ===============================================================================================================

Services: list[Service] = []

for paths in config.read():

    Services += [Service(
        module = Module(paths[0]),
        path = paths[1]
    )]

# ===============================================================================================================
