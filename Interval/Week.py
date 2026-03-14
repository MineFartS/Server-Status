from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import Path
from . import IS_SERVER

# =================================================================================
# HIDE ITEMS

def paths():
    yield from Path('C:/').descendants
    yield from Path('E:/').descendants

# Iter through all files on the 'C' and 'E' volumes
for p in paths():

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
            p.delete()

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

if IS_SERVER:

    # Iter through minecraft world dirs
    for p in Path('E:/Minecraft/Worlds').children:

        world = Service(
            'E:/Minecraft/', 
            '--World', p.name
        )

        if world.running and world.enabled:

            world.stop()
            world.start()

# =================================================================================