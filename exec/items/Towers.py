from items.Hard_Drives import HardDrives

# ===============================================================================================================

class Tower:

    def __init__(self, id:str, connected:bool):

        self.ID = id

        self.Name = f'Tower {id}'

        self.Connected = connected
        
# ===============================================================================================================

Towers: list[Tower] = []

for id in ['A', 'B', 'C']:

    for hdd in HardDrives:
        
        if (hdd.Tower == id) and hdd.Connected:
            
            Towers += [Tower(id, True)]

            break

    # If no connected hard drives are found for the tower
    else:

        # Append the tower
        Towers += [Tower(id, False)]

# ===============================================================================================================