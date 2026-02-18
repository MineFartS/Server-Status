from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.process import Run
from philh_myftp_biz.pc import Path

C = Path('C:/')
E = Path('E:/')

# =================================================================================
# HIDE ITEMS

# Iter through all files on the 'C' and 'E' volumes
for gen in (C.descendants(), E.descendants()):
    for p in gen:

        SEG  = p.seg().lower()
        PATH = str(p).lower()

        HASDOT   = SEG.startswith('.')
        MANGLED  = SEG.startswith('__') and SEG.endswith('__') 
        ISDB     = SEG in ['.ds_store', 'thumbs.db', 'desktop.ini']
        RECYCLED = '/$recycle.bin/' in PATH
        HIDDEN   = p.visibility.hidden()

        DO_HIDE = ((HASDOT or MANGLED) and (not HIDDEN))
        DO_DEL  = (ISDB or RECYCLED)

        Log.VERB(
            f'Scanning: {PATH}\n'+ \
            f'{HASDOT=} | {MANGLED=} | {ISDB=} | {RECYCLED=} | {HIDDEN=}\n'+ \
            f'{DO_HIDE=} | {DO_DEL=}'
        )

        if DO_DEL:
        # DELETE ITEM

            try:
                
                Log.INFO(f'Deleting: {PATH}')
                p.delete(force=True)

                DO_HIDE = False
                
            except PermissionError:
                Log.WARN(f'Error Deleting: {PATH}', exc_info=True)
                DO_HIDE = True

        if DO_HIDE:
        # HIDE ITEM

            if HIDDEN:
                Log.VERB(f'Already Hidden: {PATH}')

            else:
                try:
                    Log.INFO(f'Hiding: {PATH}')
                    p.visibility.hide()
                    
                except PermissionError:
                    Log.WARN(f'Error Hiding: {PATH}', exc_info=True)

# =================================================================================
# RESTART MINECRAFT

MC = Service('E:/Minecraft/')

MC.Stop()
MC.Start()

# =================================================================================
# BACKUP FILESYSTEM

syncord_dir = Path('C:/Scripts/exec/syncord/')

folders = [
    E.child('Users/philh/'), # philh
    E.child('Virtual Machines/Hyper-V/'), # Hyper-V
    E.child('Website/Root') # Root
]

for src in folders:

    Log.INFO(f'Uploading Folder: {src}')

    Run(
        ['main.py', 'upload', src],
        dir = syncord_dir,
        terminal = 'py'
    )

# =================================================================================