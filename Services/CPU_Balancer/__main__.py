from philh_myftp_biz.process.SysTask import rscan
from philh_myftp_biz.terminal import Log, cls
from philh_myftp_biz.pc import loc
from time import sleep
from os import getpid

with loc.cache.child('PID.txt').open('w') as f:
    f.write(str(getpid()))

while True:

    cls()

    for process in rscan(writeable=True):

        Log.INFO(f'{process.name()=}')
        process.cpu_limit(50)

    sleep(5)
