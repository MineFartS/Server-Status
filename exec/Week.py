from __init__ import mnt

for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        s = p.seg()

        if s.startswith('.'):
            print(p)
            p.visibility.hide()
            
        elif s.startswith('__') and s.endswith('__'):
            print(p)
            p.visibility.hide()

        elif s in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            print(p)
            p.visibility.hide()