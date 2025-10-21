from __init__ import devices, options, mnt, alert, this
from philh_myftp_biz.pc import power, Task, cls
from philh_myftp_biz.web import online, get, IP
from philh_myftp_biz import run

# ===============================================================================================================

# Clear the Terminal Window
cls()

# Remove the 'Nvidia Display Manager' Popup
Task("NVDisplay.Container").stop()

# ===============================================================================================================

# Check if server is online
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
for hdd in devices.HardDrives:

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
for vdisk in devices.VirtualDisks:

    # Check if vdisk is Unhealthy 
    if not vdisk.Healthy:

        print(f'Repairing "{vdisk.Name}" ...')

        # Repair vdisk
        run(
            f"Repair-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
            wait = True,
            terminal = 'ps',
            hide = True
        )

    # Check if vdisk is disconnected
    if not vdisk.Connected:

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

if (mnt.F.exists()) and (mnt.G.exists()):
# If mount succeeds

    # Run main startup script
#    this.run('startup/main')

    # Send alert
    alert('Startup Complete')

elif options['restart']['enabled']:
# If mount fails and restart is enabled

    # Send alert
    alert('Startup Failed - Restarting ...')

    # Show Prompt to abort shutdown
    this.start('startup/abort')

    # Restart with the configured delay
    power.restart(options['restart']['delay'])

else:
# If mount fails and restart is disabled

    # Send alert
    alert('Startup Failed')

# ===============================================================================================================
# Display a window with the system status
this.start('run', 'status', True)