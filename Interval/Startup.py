from philh_myftp_biz.modules import ServiceDisabledError
from philh_myftp_biz.process import RunHidden, SysTask
from philh_myftp_biz.terminal import Log
from .. import options, alert, this
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE

#=================

Log.INFO('Collecting Items')

from ..Items.Virtual_Disks import VirtualDisks
from ..Items.Hard_Drives import HardDrives
from ..Items.Services import Services
from ..Items.Modules import Modules

# ===============================================================================================================
# Unretire and Fix Names for Physical Disks 

Log.INFO('Initializing Hard Drives')

# Iter through Hard Drives
for hdd in HardDrives:

    Log.VERB(
        f'Found Hard Drive:\n'+ \
        f"name='{hdd.Name}'\n"+ \
        f"connected={hdd.Connected}"
    )

    # Check if disk is connected
    if hdd.Connected:
    
        # If disk's FriendlyName differs from it's intended name
        if hdd.FriendlyName != hdd.Name:

            Log.VERB(f'Renaming HDD: "{hdd.FriendlyName}" to "{hdd.Name}"')
            
            # Set the new Friendly Name
            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -NewFriendlyName '{hdd.Name}'",
                terminal = 'ps'
            )

        # If disk has a registry path 
        if hdd.RegPath:

            # Update the Friendly Name in the windows registry
            RunHidden(
                f"Set-ItemProperty '{hdd.RegPath}' FriendlyName '{hdd.Name}'",
                terminal = 'ps'
            )

        # Check if disk is retired 
        if hdd.Usage == 'Retired':

            Log.VERB(f'Reactivating HDD: {hdd.Name}')

            # Update the disk 'Usage' to 'AutoSelect'
            RunHidden(
                f"Set-PhysicalDisk -UniqueId '{hdd.UniqueID}' -Usage AutoSelect",
                terminal = 'ps'
            )

# ===============================================================================================================
# Repair and Mount Virtual Disks

Log.INFO('Initializing Virtual Disks')

# Iter through Virtual Disks
for vdisk in VirtualDisks:

    Log.VERB(
        f'Found Virtual Disk:\n'+ \
        f"name='{vdisk.Name}'\n"+ \
        f"connected={vdisk.Connected}"
    )

    # Check if vdisk is Unhealthy 
    if not vdisk.Connected:

        Log.VERB(f'Repairing VDisk: {vdisk.Name}')

        # Repair vdisk
        RunHidden(
            f"Repair-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
            terminal = 'ps'
        )

    Log.VERB(f'Mounting VDisk: {vdisk.Name}')

    # Connect vdisk
    RunHidden(
        f"Connect-VirtualDisk -UniqueId '{vdisk.UniqueID}'",
        terminal = 'ps'
    )

# ===============================================================================================================
# Send Notification with Startup Status

if Path('E:/').exists:
# If mount succeeds

    Log.INFO('Installing Modules')

    # Iter through all main modules
    for mod in Modules:

        Log.VERB(f'Installing Module: {mod}')

        # Install/Update all dependencies
        mod.install(
            show = VERBOSE
        )

    Log.INFO('Starting Services')

    # Start All Services
    for service in Services:

        Log.VERB(f'Starting Service: {service}')

        try:
            service.start()

        except ServiceDisabledError as e:
            Log.FAIL('', exc_info=True)

    # Remove the 'Nvidia Display Manager' Popup
    SysTask("NVDisplay.Container.exe").stop()

    # Send alert
    alert('Startup Complete')

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
