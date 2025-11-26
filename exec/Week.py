from __init__ import mnt
from philh_myftp_biz.pc import Path, print

def hide(path:Path):
    try:
        path.visibility.hide()
        print(path, color='GREEN')
        
    except PermissionError:
        print(path, color='RED')

for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        s = p.seg()

        if s.startswith('.'):
            hide(p)
            
        elif s.startswith('__') and s.endswith('__'):
            hide(p)

        elif s in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            hide(p)