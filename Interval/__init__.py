from philh_myftp_biz.process import RunHidden
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.web import URL
from philh_myftp_biz.pc import NAME
from ..Items import Modules

IS_SERVER: bool = (NAME == 'PC-1')

def restart() -> None:

    # Show Prompt to abort shutdown
    Modules[0].start('vbs/abort')

    # Restart the Server
    RunHidden([
        'shutdown',
        '/r',
        '/t', 30
    ])

def alert(msg:str) -> None:

    Log.MAIN(msg)

    # Show Alert Box
    Modules[0].start('vbs/alert', msg)

    if IS_SERVER:
        url = URL("https://script.google.com/macros/s/AKfycby9Xe6d1WYiMMxyHJhK7KADTucfScyvDJa5SLBGuR9QqCwrx52dRhizI2d0UjiJY_NfAg/exec")
        url.params = {'message': msg}
        url.get()
