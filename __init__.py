from philh_myftp_biz.web import online, get
from philh_myftp_biz.modules import Module
from philh_myftp_biz.file import YAML

this = Module('C:/Scripts')

options = YAML(this.file('options')).read()

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