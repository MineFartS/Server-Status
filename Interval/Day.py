from philh_myftp_biz.pc import WindowsService

#====================================================
# DISABLE WINDOWS UPDATE

WindowsService('wuauserv').disable()

WindowsService('bits').disable()

WindowsService('dosvc').disable()

#====================================================