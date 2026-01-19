from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import cls
from .Items.Services import Services
from shlex import split

# Session Memory
mem = {}

print(f"""
|---------------------------|
        Phil's Server
      [philh.myftp.biz]

     MANAGEMENT  CONSOLE
|---------------------------|
""")

while True:

    args = split(input('\n\\> ').lower())

    #===========================================
    # EXIT

    if   args[0] == 'exit':
        exit()

    #===========================================
    # CLS

    elif args[0] == 'cls':
        cls()

    #===========================================
    # HELP

    elif args[0] == 'help':
        print("""
           
              
              
        """)

    #===========================================
    # LIST

    elif args[0] == 'list':

        #===========================================
        # LIST SERVICE

        if args[1] == 'service':

            for x, serv in enumerate(Services):

                print(x, '-', serv.path)

        #===========================================

    #===========================================
    # SELECT

    elif args[0] == 'select':

        #===========================================
        # SELECT SERVICE
            
        if args[1] == 'service':

            serv = Services[int(args[2])]

            print('Selected Service:', serv.path)

            mem['service'] = serv

        #===========================================

    #===========================================
    # START

    elif args[0] == 'start':
            
        #===========================================
        # START SERVICE

        if args[1] == 'service':

            serv: Service = mem['service']

            print(' .. Starting Service ..')

            serv.Start()

        #===========================================

    #===========================================
    # STOP

    elif args[0] == 'stop':
            
        #===========================================
        # STOP SERVICE
            
        if args[1] == 'service':

            serv: Service = mem['service']

            print(' .. Stopping Service ..')

            serv.Stop()

        #===========================================

    #===========================================
    # STATUS

    elif args[0] == 'status':
            
        #===========================================
        # RUNNING SERVICE

        if args[1] == 'service':

            serv: Service = mem['service']

            if serv.Running():

                print(' .. Service is Running ..')

            else:

                print(' .. Service is Stopped ..')

        #===========================================

    #===========================================
    # ENABLE

    elif args[0] == 'enable':
            
        #===========================================
        # RUNNING SERVICE

        if args[1] == 'service':

            serv: Service = mem['service']

            # TODO

        #===========================================

    #===========================================
    # DISABLE

    elif args[0] == 'disable':
            
        #===========================================
        # RUNNING SERVICE

        if args[1] == 'service':

            serv: Service = mem['service']

            # TODO

        #===========================================