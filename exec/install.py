from importlib.util import find_spec
from pip._internal import main

if find_spec('philh_myftp_biz') is None:
    main(['install', 'philh_myftp_biz'])

from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import Path

for p in Path('E:/').children():
    
    try:
        Module(p).install(False)
    
    except ModuleNotFoundError:
        pass
