from philh_myftp_biz.pc import Path
from typing import Generator
from .Types import Mount

Mounts: list[Mount] = [

    Mount('C:/'),

    Mount('E:/')

]

def all_paths() -> Generator[Path]:

    for mnt in Mounts:

        yield from mnt.descendants
