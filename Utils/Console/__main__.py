from philh_myftp_biz.terminal import warn
from philh_myftp_biz.text import split
from .Commands import Tree
from .Types import Printer

Tree.cls()

while True:

    try:

        args = split(input('\n\\> ').lower())

        Tree(*args)

    except ValueError:
        pass

    except KeyboardInterrupt:
        Printer.Error('KeyboardInterrupt')

    except Exception as e:
        warn(e)
