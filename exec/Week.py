from philh_myftp_biz.pc import print
from __init__ import mnt

# =================================================================================

# Iter through all files on the 'C' and 'E' volumes
for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        s = p.seg()

        if not s.startswith('.'):
            continue
            
        elif not (s.startswith('__') and s.endswith('__')):
            continue

        elif s not in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            continue

        else:

            try:
                p.visibility.hide()
                print(p, color='GREEN')
                
            except PermissionError:
                print(p, color='RED')

# =================================================================================