from philh_myftp_biz.process.SysTask import rscan
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.pc import loc
from random import sample
from os import getpid

with loc.cache.child('PID.txt').open('w') as f:
    f.write(str(getpid()))

while True:
    for process in rscan(writeable=True):

        src = process.cpu_affinity()

        if len(src) > 2:
            dst = sample(src, 2)
            Log.INFO(f'{process.name()}\n{src=}\n{dst=}')
            process.cpu_affinity(dst)

