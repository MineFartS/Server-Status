from philh_myftp_biz.modules import ServiceDisabledError
from philh_myftp_biz.process import RunHidden, SysTask
from philh_myftp_biz.terminal import Log, ParsedArgs
from .. import options, alert, this
from philh_myftp_biz.pc import Path
from philh_myftp_biz import VERBOSE

#=================

from ..Items.Virtual_Disks import VirtualDisks
from ..Items.Hard_Drives import HardDrives
from ..Items.Services import Services
from ..Items.Modules import Modules

#=================

args = ParsedArgs()

args.Flag(
    name = 'quick',
    letter = 'q'
)

# ===============================================================================================================
# Unretire and Fix Names for Physical Disks 

if not args['quick']:

    Log.INFO('Processing Hard Drives')

    # Iter through Hard Drives
    for hdd in HardDrives:

        Log.VERB(
            f'Processing Hard Drive:\n'+ \
            f"name='{hdd.Name}'\n"+ \
            f"connected={hdd.Connected}"
        )

        # Check if disk is connected
        if hdd.Connected:
        
            # If disk's FriendlyName differs from it's intended name
            if hdd.FriendlyName != hdd.Name:

                Log.VERB(f'Renaming HDD: "{hdd.FriendlyName}" to "{hdd.Name}"')
                
                hdd.FriendlyName = hdd.Name

            # Check if disk is retired 
            if hdd.Usage == 'Retired':

                Log.VERB(f'Reactivating HDD: {hdd.Name}')

                hdd.Usage = 'Auto-Select'

# ===============================================================================================================
# Repair and Mount Virtual Disks

Log.INFO('Processing Virtual Disks')

# Iter through Virtual Disks
for vdisk in VirtualDisks:

    Log.VERB(
        f'Processing Virtual Disk:\n'+ \
        f"name='{vdisk.Name}'\n"+ \
        f"connected={vdisk.Connected}"
    )

    # Check if vdisk is Unhealthy 
    if not vdisk.Connected:

        Log.VERB(f'Repairing VDisk: {vdisk.Name}')

        vdisk.repair()

    if not vdisk.Mounted:

        Log.VERB(f'Mounting VDisk: {vdisk.Name}')

        vdisk.Mounted = True

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
