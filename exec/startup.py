from philh_myftp_biz.web import online, get, IP
from __init__ import options, mnt, alert, this
from philh_myftp_biz.modules import Scanner
from philh_myftp_biz.pc import Task
from philh_myftp_biz import run

from items.Virtual_Disks import VirtualDisks
from items.Hard_Drives import HardDrives
from items.Services import Services

# ===============================================================================================================

# if server is online
if online():

    # Update IP Address Registry with current active IP
    get(
        url = 'https://script.google.com/macros/s/AKfycbx4POaZ4dAKsPtlNZLFTf5_HkCCx8HM8DhznDoop7radoV-Amgzix7aMl2c9lZ0MbqyaA/exec',
        params = {
            'pc': 1,
            'ip': IP('public')
        }
    )

# ===============================================================================================================
# Unretire and Fix Names for Physical Disks 

# Iter through Hard Drives
for hdd in HardDrives:

    # Check if disk is connected
    if hdd.Connected:
    
        # Check if disks FriendlyName differs from it's intended name
        if hdd.FriendlyName != hdd.Name:

            print(f'Renaming "{hdd.FriendlyName}" to "{hdd.Name}" ...')
            
            # Set the new Friendly Name
            run(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -NewFriendlyName '{hdd.Name}'",
                wait = True,
                terminal = 'ps',
                hide = True
            )

        # Check if disk is retired 
        if hdd.Usage == 'Retired':

            print(f'Reactivating "{hdd.Name}" ...')

            # Update the disk 'Usage' to 'AutoSelect'
            run(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -Usage AutoSelect",
                wait = True,
                terminal = 'ps',
                hide = True
            )

# ===============================================================================================================
# Repair and Mount Virtual Disks

# Iter through Virtual Disks
for vdisk in VirtualDisks:

    # Check if vdisk is Unhealthy 
    if not vdisk.Connected:

        print(f'Repairing "{vdisk.Name}" ...')

        # Repair vdisk
        run(
            f"Repair-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
            wait = True,
            terminal = 'ps',
            hide = True
        )

    print(f'Mounting "{vdisk.Name}" ...')

    # Connect vdisk
    run(
        f"Connect-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
        wait = True,
        terminal = 'ps',
        hide = True
    )

# ===============================================================================================================
# Send Notification with Startup Status

if mnt.E.exists():
# If mount succeeds

    # Send alert
    alert('Startup Complete')

    # Iter through all main modules
    for m in Scanner():

        # Install/Update all dependencies
        m.install(hide=False)

    # Start All Services
    for service in Services:
        service.Start(force=True)

    # Remove the 'Nvidia Display Manager' Popup
    Task("NVDisplay.Container.exe").stop()

elif options['restart']['enabled']:
# If mount fails and restart is enabled

    # Send alert
    alert('Startup Failed - Restarting ...')

    # Show Prompt to abort shutdown
    this.start('exec/abort')

    # Restart with the configured delay
    run([
        'shutdown',
        '/r',
        '/t', options['restart']['delay']
    ])

else:
# If mount fails and restart is disabled

    # Send alert
    alert('Startup Failed')

# ===============================================================================================================

# Open a new window with the system status
this.start('run', 'status', True)
