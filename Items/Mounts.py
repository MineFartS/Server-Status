from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import Path
from typing import Generator

Log.VERB('Collecting Mounts')

# ===============================================================================================================
# CONFIGURATION

Mounts: list[Path] = [

    Path('C:/'),

    Path('E:/')

]

# ===============================================================================================================

def all_paths() -> Generator[Path]:

    for mnt in Mounts:

        yield from mnt.descendants

# ===============================================================================================================