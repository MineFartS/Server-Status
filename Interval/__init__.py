from philh_myftp_biz.process import RunHidden
from ..Items import Modules
from typing import NoReturn

def restart() -> NoReturn:

    # Show Prompt to abort shutdown
    Modules[0].start('vbs/abort')

    # Restart the Server
    RunHidden([
        'shutdown',
        '/r',
        '/t', 30
    ])

    exit()
