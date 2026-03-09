from philh_myftp_biz.terminal import warn
from philh_myftp_biz.text import split
from .Commands import Tree
from .Types import Printer

Tree.cls()

while True:

    try:

        args: list[str] = split(input('\n\\> ').lower())

        if len(args) > 0:
            Tree(*args)

    except KeyboardInterrupt:
        Printer.Error('KeyboardInterrupt')

    except Exception as e:
        warn(e)
