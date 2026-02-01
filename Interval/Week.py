from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import Path

# =================================================================================

C = Path('C:/').descendants()
E = Path('E:/').descendants()

# Iter through all files on the 'C' and 'E' volumes
for gen in (C, E):
    for p in gen:

        SEG  = p.seg().lower()
        PATH = str(p).lower()

        HASDOT   = SEG.startswith('.')
        MANGLED  = SEG.startswith('__') and SEG.endswith('__') 
        ISDB     = SEG in ['.ds_store', 'thumbs.db', 'desktop.ini']
        RECYCLED = '/$recycle.bin/' in PATH
        HIDDEN   = p.visibility.hidden()

        Log.VERB(f'Scanning: {PATH}\n{HASDOT=} | {MANGLED=} | {ISDB=} | {RECYCLED=} | {HIDDEN=}')

        DO_HIDE = ((HASDOT or MANGLED) and (not HIDDEN))
        DO_DEL  = (ISDB or RECYCLED)

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