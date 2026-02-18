from philh_myftp_biz.pc import Path
from philh_myftp_biz.process import Run

syncord_dir = Path('C:/Scripts/exec/syncord/')

E = Path('E:/')

E.cd()

for src in E.children():

    VISIBLE  = (not src.visibility.hidden())
    FILE     = src.isfile()
    NOTTRASH = ('/$RECYCLE.BIN/' not in str(src))

    if all([VISIBLE, NOTTRASH]) :

        rel = ':'.join(str(src).split(':')[1:])

        #dst = '/' + str(src).replace(':', '', 1)

        print('')
        print(f'{src=}')
        print(f'{rel=}')

        Run(
            ['main.py', 'upload', src],
            dir = syncord_dir,
            terminal = 'py'
        )

        exit()