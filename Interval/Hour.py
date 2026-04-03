from philh_myftp_biz.web import FirewallException
from philh_myftp_biz.terminal import Log
from ..Items import Services, Modules
from philh_myftp_biz.time import now
from philh_myftp_biz.pc import Path
from . import IS_SERVER

# ==================================================
# FIREWALL

FirewallException('RDP').set(3389)
FirewallException('SSH').set(22)

# ==================================================
# SERVICES

# Ensure all Services are Running
for service in Services:

    if (not service.running) and service.enabled:
        
        service.start()

# ==================================================
# MINECRAFT

if IS_SERVER:

    # Backup Minecraft Worlds
    Modules[2].run('Backup')

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