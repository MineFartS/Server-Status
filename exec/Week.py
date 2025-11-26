from __init__ import mnt
from philh_myftp_biz.pc import Path

def hide(path:Path):    
    try:
        path.visibility.hide()
        print(path)
    except PermissionError:
        pass

for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        s = p.seg()

        if s.startswith('.'):
            hide(p)
            
        elif s.startswith('__') and s.endswith('__'):
            hide(p)

        elif s in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            hide(p)