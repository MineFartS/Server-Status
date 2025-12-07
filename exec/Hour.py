from philh_myftp_biz.web import online
from philh_myftp_biz.time import now
from __init__ import wifi, services
from philh_myftp_biz.pc import Path

# ==================================================

# If the server is disconnected from the internet
if not online():

    # Connect to wifi
    wifi.connect('FiOS-6AMDP')

# ==================================================

# Ensure all Services are Running
for service in services:
    service.Start()

# ==================================================

temp = Path('E:/__temp__')

minAge = (now().unix - 43200) # 12 hours ago

# Get all files in the temp dir
for p in temp.descendants():

    #
    if p.isfile():
    
        # If file is more than 12 hours old
        if p.mtime.get() < minAge:

            # Delete File
            p.delete()

# ==================================================