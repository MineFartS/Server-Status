from philh_myftp_biz.web import online, get, WiFi
from philh_myftp_biz.modules import Module
from philh_myftp_biz.file import YAML
from philh_myftp_biz.pc import Path

# ===============================================================================================================

this = Module('C:/Scripts/')

try:
    AI = Module('E:/AI/')
    Web = Module('E:/Website/')
    Plex = Module('E:/Plex/')
except ModuleNotFoundError:
    AI = None
    Web = None
    Plex = None

options = YAML(this.file('config/options')).read()

class mnt:
    C = Path('C:/')
    E = Path('E:/')
    D = Path('D:/')

wifi = WiFi()

# ===============================================================================================================

def alert(m):

    if online() and options['alert']['sms']:
        # Send SMS Alert
        get(
            url = 'https://script.google.com/macros/s/AKfycbztUPSGrf9lnl3_qIBjBui6pDSl_errjxdEi_9LnGNO0TjgMeZDBvWvrQBU36P80x0/exec',
            params = {'message' : m}
        )

    if options['alert']['popup']:
        # Show Alert Box
        this.start('exec/alert', m)

# ===============================================================================================================
