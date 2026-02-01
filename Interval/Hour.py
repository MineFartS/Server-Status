from philh_myftp_biz.modules import ServiceDisabledError
from ..Items.Services import Services
from philh_myftp_biz.time import now
from philh_myftp_biz.pc import Path
from philh_myftp_biz.terminal import Log

# ==================================================

# Ensure all Services are Running
for service in Services:
    
    try:
        service.Start(force=False)
    
    except ServiceDisabledError:
        pass

# ==================================================

temp = Path('E:/__temp__')

MINIMUM = (now().unix - 3600*20) # 20 hours ago

# Get all files in the temp dir
for p in temp.descendants():
    if p.isfile():

        MODIFIED = p.mtime.get()
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
            p.delete(force=True)

# ==================================================