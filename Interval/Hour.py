from philh_myftp_biz.modules import Module
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.time import now
from philh_myftp_biz.pc import Path
from ..Items import Services

# ==================================================
# SERVICES

# Ensure all Services are Running
for service in Services:

    if (not service.running) and service.enabled:
        
        service.start()

# ==================================================
# MINECRAFT

MC = Module('E:/Minecraft')

# Backup Minecraft Worlds
MC.run('Backup')

# ==================================================
# CLEAN TEMP

temp = Path('E:/__temp__')

MINIMUM = (now().unix - 3600*20) # 20 hours ago

# Get all files in the temp dir
for p in temp.descendants:
    if p.is_file:

        MODIFIED = p.mtime.current

        DIFF     = (MINIMUM - MODIFIED.unix)

        DELETE = (DIFF > 0)

        Log.INFO(
            f'Scanning File\n'+ \
            f'{str(p)=}\n'+ \
            f'{MODIFIED.ISO=}\n' +\
            f'{DIFF=}\n'+ \
            f'{DELETE=}'
        )
    
        if DELETE:
            # Delete File
            p.delete()

# ==================================================