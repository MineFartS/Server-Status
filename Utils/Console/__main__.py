from philh_myftp_biz.terminal import warn
from philh_myftp_biz.text import split
from .Commands import CommandTree

CommandTree.cls()

while True:

    try:

        args = split(input('\n\\> ').lower())

        CommandTree(*args)

    except KeyboardInterrupt:
        
        print('\n<KeyboardInterrupt>')

    except Exception as e:

        warn(e)
