from ..Items import VirtualDisks, HardDrives, Services, Modules, PCIeCards, Mounts
from philh_myftp_biz.modules import ServiceDisabledError
from philh_myftp_biz.process import SysTask
from philh_myftp_biz.terminal import Log
from philh_myftp_biz import VERBOSE
from . import alert, restart

# ===============================================================================================================

Log.INFO('Checking for issues with PCIe Cards')

if not all(c.Connected for c in PCIeCards):
    
    # Send alert
    alert('Restarting due to PCIe card error')

    restart()

# ===============================================================================================================

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

Log.INFO('Installing Modules')

# Iter through all main modules
for mod in Modules:

    Log.VERB(f'Installing Module: {mod}')

    # Install/Update all dependencies
    mod.install(
        show = VERBOSE
    )

# ===============================================================================================================

Log.INFO('Checking for issues with Mounts')

if not Mounts[1].exists:

    _failed = filter(
        lambda d: not d.Connected,
        HardDrives
    )

    failed = [f'{d.ID:02d}-{d.Tower}' for d in _failed]

    alert(f'Restarting due to Hard Drive Failure: {failed}')

    restart()

# ===============================================================================================================

Log.INFO('Starting Services')

# Start All Services
for service in Services:

    try:
        service.start()

    except ServiceDisabledError as e:
        Log.FAIL('', exc_info=True)

# ===============================================================================================================

# Send alert
alert('Startup Complete')

# Remove the 'Nvidia Display Manager' Popup
SysTask("*NVDisplay*").stop()

# ===============================================================================================================
