from philh_myftp_biz.process import RunHidden, SysTask
from .. import options, alert, this
from philh_myftp_biz.pc import Path

from ..Items.Virtual_Disks import VirtualDisks
from ..Items.Hard_Drives import HardDrives
from ..Items.Services import Services
from ..Items.Modules import Modules

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
            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -NewFriendlyName '{hdd.Name}'",
                terminal = 'ps'
            )

        # Check if disk is retired 
        if hdd.Usage == 'Retired':

            print(f'Reactivating "{hdd.Name}" ...')

            # Update the disk 'Usage' to 'AutoSelect'
            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -Usage AutoSelect",
                terminal = 'ps'
            )

# ===============================================================================================================
# Repair and Mount Virtual Disks

# Iter through Virtual Disks
for vdisk in VirtualDisks:

    # Check if vdisk is Unhealthy 
    if not vdisk.Connected:

        print(f'Repairing "{vdisk.Name}" ...')

        # Repair vdisk
        RunHidden(
            f"Repair-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
            terminal = 'ps'
        )

    print(f'Mounting "{vdisk.Name}" ...')

    # Connect vdisk
    RunHidden(
        f"Connect-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
        terminal = 'ps'
    )

# ===============================================================================================================
# Send Notification with Startup Status

if Path('E:/').exists():
# If mount succeeds

    # Send alert
    alert('Startup Complete')

    # Iter through all main modules
    for mod in Modules:

        # Install/Update all dependencies
        mod.install()

    # Start All Services
    for service in Services:
        service.Start(force=True)

    # Remove the 'Nvidia Display Manager' Popup
    SysTask("NVDisplay.Container.exe").stop()

elif options['restart']['enabled']:
# If mount fails and restart is enabled

    # Send alert
    alert('Startup Failed - Restarting ...')

    # Show Prompt to abort shutdown
    this.start('exec/abort')

    # Restart with the configured delay
    RunHidden([
        'shutdown',
        '/r',
        '/t', options['restart']['delay']
    ])

else:
# If mount fails and restart is disabled

    # Send alert
    alert('Startup Failed')

# ===============================================================================================================
