from philh_myftp_biz.terminal import Log
from philh_myftp_biz.web import get
from ..Items import Modules

def alert(msg:str) -> None:

    Log.MAIN(msg)

    # Send SMS Alert
    get(
        url = 'https://script.google.com/macros/s/AKfycbyKYV2-Q1JUtMr1FdKR5eP-Bxy5m1EOd8EOFH9ghueqN-zZqQpPa9PEi8ZFz5T5uQc1Xg/exec',
        params = {'message': msg}
    )

    # Show Alert Box
    Modules[0].start('vbs/alert', msg)
