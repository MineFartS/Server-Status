from .Types import PCIeCard

PCIeCards = [

    PCIeCard(
        Slot = 1,
        Lanes = 1,
        DeviceID = "PCI\\VEN_1B21&DEV_2142&SUBSYS_21421B21&REV_00\\4&33FC7E38&0&00E0"
    ),

    PCIeCard(
        Slot = 2,
        Lanes = 16,
        DeviceID = "PCI\\VEN_10DE&DEV_13BA&SUBSYS_109710DE&REV_A2\\4&787313E&0&0008"
    ),

    PCIeCard(
        Slot = 3,
        Lanes = 4,
        DeviceID = "PCI\\VEN_1B21&DEV_1064&SUBSYS_21161B21&REV_02\\4&F6FAD87&0&00E8"
    ),

    PCIeCard(
        Slot = 'M.2',
        Lanes = 4,
        DeviceID = "PCI\\VEN_1B21&DEV_1166&SUBSYS_21162116&REV_02\\4&1E804E93&0&00D8"
    )

]

# ===============================================================================================================