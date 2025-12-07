from philh_myftp_biz.web import online
from philh_myftp_biz.time import now
from philh_myftp_biz.pc import Path
from __init__ import wifi, Web

# ==================================================

# If the server is disconnected from the internet
if not online():

    # Connect to wifi
    wifi.connect('FiOS-6AMDP')

# ==================================================

# Run the Website Indexer
Web.run('Indexer/run')

# If the website API service is not running
if not Web.run('API/Running').output('json'):
    
    # Start the website API service
    Web.run('API/Start')

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