from philh_myftp_biz.web import online
from philh_myftp_biz.time import now
from __init__ import wifi, Web, Plex
from philh_myftp_biz.pc import Path

# ==================================================

# If the server is disconnected from the internet
if not online():

    # Connect to wifi
    wifi.connect('FiOS-6AMDP')

# ==================================================

# If the Website Indexing Service is not running
if not Web.cap('Indexer/Running'):

    # Start the Website Indexing Service
    Web.run('Indexer/Start')

# If the Website API Service is not running
if not Web.cap('API/Running'):
    
    # Start the website API service
    Web.run('API/Start')

# If the Plex Torrenting Service is not running
if not Plex.cap('Torrenting/Running'):

    # Start Plex Torrenting Service
    Plex.run('Torrenting/Run')

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