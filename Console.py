#=================================================================================
from sys import executable
from subprocess import run

run(
    args = [executable, '-m', 'pip', 'install', '.'],
    cwd = 'C:/Users/Administrator/Documents/GitHub/philh_myftp_biz/'
)

#=================================================================================

from philh_myftp_biz.modules import Service
from philh_myftp_biz.terminal import cls
from philh_myftp_biz.text import split
from .Items.Services import Services
from . import this

from philh_myftp_biz.process import SysTask

# Session Memory
mem = {}

#===========================================================================

def run(*args:str) -> None:

    if len(args) == 0:
        
        print("""
NO COMMAND GIVEN

Type 'help' for a list of commands
""")
        
        return
    
    match args[0]:

        #===========================================
        case 'exit':
        # EXIT
        
            exit() 

        #===========================================
        case 'cls':
        # CLS

            cls()

            print(f"""
|---------------------------|
        Phil's Server
    [philh.myftp.biz]

    MANAGEMENT  CONSOLE
|---------------------------|

Type 'help' for a list of commands
""")

        #===========================================
        case 'help':
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
ARGS    | Set arguements

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
            elif args[1] == 'args':
            # HELP ARGS

                print("""
ARGS SERVICE = *arg1* *arg2* ...   | Set the args for the selected service
""")

        #===========================================
        case 'list':
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

                        RUNNING = ('Running' if serv.running else 'Stopped')
                        ENABLED = (' Enabled' if serv.enabled else 'Disabled')

                        print(f'{x}: [{RUNNING}, {ENABLED}] {serv.path} ')

            #===========================================

        #===========================================
        case 'select':
        # SELECT

            #===========================================            
            if args[1] == 'service':
            # SELECT SERVICE

                serv = Services[int(args[2])]

                print('Selected Service:', serv.path)

                mem['service'] = serv

            #===========================================

        #===========================================
        case 'start':
        # START
                
            #===========================================
            if args[1] == 'service':
            # START SERVICE

                serv: Service = mem['service']

                print(f'Running Script: {serv.file('Start')}')
                print(f'Arguements: {serv.args}')

                serv.start(force=True)

            #===========================================

        #===========================================
        case 'stop':
        # STOP
                
            #===========================================            
            if args[1] == 'service':
            # STOP SERVICE

                serv: Service = mem['service']

                print(f'Running Script: {serv.file('Stop')}')

                serv.stop()

            #===========================================

        #===========================================
        case 'status':
        # STATUS
                
            #===========================================
            if args[1] == 'service':
            # STATUS SERVICE

                serv: Service = mem['service']

                RUNNING = str(serv.running)

                ENABLED = str(serv.enabled)

                print(f"""
Running: {RUNNING}
Enabled: {ENABLED}
""")

            #===========================================

        #===========================================
        case 'enable':
        # ENABLE
                
            #===========================================
            if args[1] == 'service':
            # ENABLE SERVICE

                serv: Service = mem['service']
                
                print('Enabling Service ...')

                serv.enable()

            #===========================================

        #===========================================
        case 'disable':
        # DISABLE
                
            #===========================================
            if args[1] == 'service':
            # DISABLE SERVICE

                serv: Service = mem['service']

                print('Disabling Service ...')

                serv.disable()

            #===========================================

        #===========================================
        case 'run':
        # RUN

            print(f'Running Script: C:/Scripts/{args[1].replace('.', '/')}.py')
            print(f'Arguements: {args[2:]}')
            
            this.run(
                'run', args[1].title(), 
                'True', # VISIBLE
                ('-v' in args) # VERBOSE
            )

            #===========================================

        #===========================================
        case 'args':
        # ARGS

            #===========================================
            if args[1] == 'service':
            # ARGS SERVICE

                mem['service'].args = args[3:]

                print('Updated Arguements ...')

        #===========================================
        case 'terminate':
        # TERMINATE

            PIDs = []

            PIDs += SysTask('python.exe').PIDs

            PIDs += SysTask('geckodriver.exe').PIDs

            PIDs += SysTask('firefox.exe').PIDs

            print(PIDs)

            # TODO

        #===========================================
        case _:
        # *UNKNOWN*

            print(f"""
"{args[0]}" NOT IMPLEMENTED

Type 'help' for a list of commands
    """)

#===========================================================================

run('cls')

while True:

    try:

        rawinput = input('\n\\> ').lower()

        run(*split(rawinput))

    except KeyboardInterrupt:
        
        print('\n<KeyboardInterrupt>')

#===========================================================================