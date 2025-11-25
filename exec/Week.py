from __init__ import mnt

for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        s = p.seg()

        if s.startswith('.'):
            p.visibility.hide()
            
        elif s.startswith('__') and s.endswith('__'):
            p.visibility.hide()

        elif s in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            p.visibility.hide()