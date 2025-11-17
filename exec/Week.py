from __init__ import mnt

for gen in (mnt.E.descendants(), mnt.C.descendants()):

    for p in gen:

        if p.seg().startswith('.'):
            print(p)

        if p.isdir() and (p.name() == '__pycache__'):
            print(p)

        elif p.seg() in ['.DS_Store', 'Thumbs.db', 'desktop.ini']:            
            print(p)