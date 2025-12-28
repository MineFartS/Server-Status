from philh_myftp_biz.terminal import print
from philh_myftp_biz.pc import Path

# =================================================================================

C = Path('C:/').descendants()
E = Path('E:/').descendants()

# Iter through all files on the 'C' and 'E' volumes
for gen in (E, C):
    for p in gen:

        print(p)

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