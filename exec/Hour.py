from philh_myftp_biz.modules import Module
from philh_myftp_biz.web import online
from philh_myftp_biz.time import now
from philh_myftp_biz.pc import Path
from __init__ import wifi

# ==================================================

# If the server is disconnected from the internet
if not online():

    # Connect to the wifi network named '1337 14n'
    wifi.connect('FiOS-6AMDP')

# ==================================================

website = Module('E:/Website')

website.run('index')

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