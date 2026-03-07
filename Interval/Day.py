from philh_myftp_biz.process import Run

def disable_service(name:str):

    # Stop Service
    Run(['net', 'stop', name])

    # Disable Service
    Run(['sc', 'config', name, 'start=disabled'])

#====================================================

disable_service('wuauserv')

disable_service('bits')

disable_service('dosvc')
