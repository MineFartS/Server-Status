from philh_myftp_biz.pc import WindowsService

#====================================================

WindowsService('wuauserv').disable()

WindowsService('bits').disable()

WindowsService('dosvc').disable()
