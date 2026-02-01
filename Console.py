from philh_myftp_biz.process import RunHidden
from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import cls
from philh_myftp_biz.modules import Module
from .Items.Services import Services
from philh_myftp_biz import VERBOSE
from shlex import split


this = Module('C:/Scripts')

# Session Memory
mem = {}

print(f"""
|---------------------------|
        Phil's Server
      [philh.myftp.biz]

     MANAGEMENT  CONSOLE
|---------------------------|

Type 'help' for a list of commands
""")

while True:

    args = split(input('\n\\> ').lower())

    if len(args) == 0:
        print("""
NO COMMAND GIVEN

Type 'help' for a list of commands
""")
    
    #===========================================
    elif args[0] == 'exit':
    # EXIT
    
        exit()

        raise 

    #===========================================
    elif args[0] == 'cls':
    # CLS

        cls()

    #===========================================
    elif args[0] == 'help':
        if len(args) == 1:
    # HELP
        
            print("""
----------------------------------------

CLS  | Clear the Terminal
EXIT | Exit the terminal

----------------------------------------

LIST    | List items
SELECT  | Select an item
START   | Start an item
STOP    | Stop an item
STATUS  | Get the status of an item
ENABLE  | Enable an item
DISABLE | Disable an item
RUN     | Run a script

Run 'help *cmd*' for more details about a specific command

----------------------------------------
""")

        #===========================================
        elif args[1] == 'list':
        # HELP LIST

            print("""
LIST SERVICE      | Get a list of services
LIST SERVICE FULL | Get a detailed list of services
""")

        #===========================================
        elif args[1] == 'select':
        # HELP SELECT

            print("""
SELECT SERVICE # | Select a service by number 
""")

                #===========================================
        elif args[1] == 'start':
        # HELP START

            print("""
START SERVICE | Start the selected service
""")

                #===========================================
        elif args[1] == 'stop':
        # HELP STOP

            print("""
STOP SERVICE | Stop the selected service
""")

        #===========================================
        elif args[1] == 'status':
        # HELP STATUS

            print("""
STATUS SERVICE | Get the status of the selected service 
""")

                #===========================================
        elif args[1] == 'enable':
        # HELP ENABLE

            print("""
ENABLE SERVICE | Enable the selected service
""")

        #===========================================
        elif args[1] == 'disable':
        # HELP DISABLE

            print("""
DISABLE SERVICE | Disable the selected service 
""")

                #===========================================
        elif args[1] == 'run':
        # HELP RUN

            print("""
RUN *SCRIPT*    | Run a script in a new tab (Ex: run Interval.Startup)
RUN *SCRIPT* -v | Run a script in a new tab with the verbose flag (Ex: run Interval.Startup -v)
""")

    #===========================================
    elif args[0] == 'list':
    # LIST

        #===========================================
        if args[1] == 'service':
            if len(args) == 2:
        # LIST SERVICE
                
                for x, serv in enumerate(Services):
                    print(f'{x}: {serv.path} ')

            #===========================================
            elif args[2] == 'full':
            # LIST SERVICE FULL

                for x, serv in enumerate(Services):

                    RUNNING = ('Running' if serv.Running() else 'Stopped')
                    ENABLED = (' Enabled' if serv.Enabled() else 'Disabled')

                    print(f'{x}: [{RUNNING}, {ENABLED}] {serv.path} ')

        #===========================================

    #===========================================
    elif args[0] == 'select':
    # SELECT

        #===========================================            
        if args[1] == 'service':
        # SELECT SERVICE

            serv = Services[int(args[2])]

            print('Selected Service:', serv.path)

            mem['service'] = serv

        #===========================================

    #===========================================
    elif args[0] == 'start':
    # START
            
        #===========================================
        if args[1] == 'service':
        # START SERVICE

            serv: Service = mem['service']

            print(' .. Starting Service ..')

            serv.Start(force=True)

        #===========================================

    #===========================================
    elif args[0] == 'stop':
    # STOP
            
        #===========================================            
        if args[1] == 'service':
        # STOP SERVICE

            serv: Service = mem['service']

            print(' .. Stopping Service ..')

            serv.Stop()

        #===========================================

    #===========================================
    elif args[0] == 'status':
    # STATUS
            
        #===========================================
        if args[1] == 'service':
        # STATUS SERVICE

            serv: Service = mem['service']

            RUNNING = str(serv.Running())

            ENABLED = str(serv.Enabled())

            print(f"""
|================|
| Running: {RUNNING:5} |
| Enabled: {ENABLED:5} |   
|================|""")

        #===========================================

    #===========================================
    elif args[0] == 'enable':
    # ENABLE
            
        #===========================================
        if args[1] == 'service':
        # ENABLE SERVICE

            serv: Service = mem['service']

            serv.Enable()

        #===========================================

    #===========================================
    elif args[0] == 'disable':
    # DISABLE
            
        #===========================================
        if args[1] == 'service':
        # DISABLE SERVICE

            serv: Service = mem['service']

            serv.Disable()

        #===========================================

    #===========================================
    elif args[0] == 'run':
    # RUN

        this.run(
            'run', args[1].title(), 
            'True', # VISIBLE
            ('-v' in args) # VERBOSE
        )

        #===========================================

    #===========================================
    else:
    # *UNKNOWN*

        print(f"""
"{args[0]}" NOT IMPLEMENTED

Type 'help' for a list of commands
""")
