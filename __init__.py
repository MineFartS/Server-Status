
try:
    import philh_myftp_biz # pyright: ignore[reportUnusedImport]
except ModuleNotFoundError:
    from . import Setup # pyright: ignore[reportUnusedImport]

from philh_myftp_biz.web import is_online, get
from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.file import YAML

this = Module('C:/Scripts')

options: dict = YAML(this.file('options')).read()

def alert(m:str) -> None:

    Log.INFO(f'Alert: {m}')

    if is_online() and options['alert']['sms']:
        # Send SMS Alert
        get(
            url = 'https://script.google.com/macros/s/AKfycbyKYV2-Q1JUtMr1FdKR5eP-Bxy5m1EOd8EOFH9ghueqN-zZqQpPa9PEi8ZFz5T5uQc1Xg/exec',
            params = {'message' : m}
        )

    if options['alert']['popup']:
        # Show Alert Box
        this.start('exec/alert', m)