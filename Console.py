from philh_myftp_biz.text import split, to_slice
from philh_myftp_biz.terminal import cls, warn
from philh_myftp_biz.modules import Service
from .Items import Services, Modules

#=============

# Session Memory
mem = {
    'service': Services.copy(),
    'module': Modules.copy()
}

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
CHECK   | Get the status of an item
ENABLE  | Enable an item
DISABLE | Disable an item
RUN     | Run a script
ARGS    | Set arguements for an item

Run 'help *cmd*' for more details about a specific command

----------------------------------------
""")

            #===========================================
            elif args[1] == 'list':
            # HELP LIST

                print("""
LIST SERVICE      | Get a list of services
LIST MODULE       | Get a list of modules
""")

            #===========================================
            elif args[1] == 'select':
            # HELP SELECT

                print("""
SELECT SERVICE [#|#..|..#|#..#|#,#] | Select services (Ex: select service 1,3)
SELECT MODULE  [#|#..|..#|#..#|#,#] | Select modules (Ex: select module ..5)
""")

            #===========================================
            elif args[1] == 'start':
            # HELP START

                print("""
START SERVICE | Start the selected services
""")

            #===========================================
            elif args[1] == 'stop':
            # HELP STOP

                print("""
STOP SERVICE | Stop the selected services
""")

            #===========================================
            elif args[1] == 'check':
            # HELP STATUS

                print("""
CHECK SERVICE | Get the status of the selected services
""")

            #===========================================
            elif args[1] == 'enable':
            # HELP ENABLE

                print("""
ENABLE SERVICE | Enable the selected services
""")

            #===========================================
            elif args[1] == 'disable':
            # HELP DISABLE

                print("""
DISABLE SERVICE | Disable the selected services
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
ARGS SERVICE # = *arg1* *arg2* ...   | Set the args for a specific service
""")

        #===========================================
        case 'list':
        # LIST

            #===========================================
            if args[1] == 'service':
            # LIST SERVICE
                    
                for serv in mem['service']:
                    
                    print(f'{Services.index(serv)}: {serv.path} {serv.args}')

            #===========================================
            elif args[1] == 'module':
            # LIST MODULE
                    
                for mod in mem['module']:
                    
                    print(f'{Modules.index(mod)}: {mod.path}')

            #===========================================

        #===========================================
        case 'select':
        # SELECT

            #===========================================            
            if args[1] == 'service':
            # SELECT SERVICE

                mem['service'] = []

                for s in to_slice(args[2]):

                    serv = Services[s]

                    if not isinstance(serv, list):
                        serv = [serv]

                    mem['service'] += serv

                for serv in mem['service']:

                    print(f'{Services.index(serv)}: {serv.path}')

            #===========================================            
            if args[1] == 'module':
            # SELECT MODULE

                mem['module'] = []

                for s in to_slice(args[2]):

                    mod = Modules[s]

                    if not isinstance(mod, list):
                        mod = [mod]

                    mem['module'] += mod

                for mod in mem['module']:

                    print(f'{Modules.index(mod)}: {mod.path}')

            #===========================================

        #===========================================
        case 'start':
        # START
                
            #===========================================
            if args[1] == 'service':
            # START SERVICE

                services: list[Service] = mem['service']

                for serv in services:

                    print(f'Running: {serv.file('Start')} {serv.args}')

                    serv.start(force=True)

            #===========================================

        #===========================================
        case 'stop':
        # STOP
                
            #===========================================            
            if args[1] == 'service':
            # STOP SERVICE

                services: list[Service] = mem['service']

                for serv in services:

                    print(f'Running: {serv.file('Stop')}')

                    serv.stop()

            #===========================================

        #===========================================
        case 'enable':
        # ENABLE
                
            #===========================================
            if args[1] == 'service':
            # ENABLE SERVICE

                print('Enabling Selected Services ...')

                services: list[Service] = mem['service']

                for serv in services:

                    serv.enable()

            #===========================================

        #===========================================
        case 'disable':
        # DISABLE
                
            #===========================================
            if args[1] == 'service':
            # DISABLE SERVICE

                print('Disabling Selected Services ...')

                services: list[Service] = mem['service']

                for serv in services:

                    serv.disable()

            #===========================================

        #===========================================
        case 'run':
        # RUN

            print(f'Running: C:/Scripts/{args[1].replace('.', '/')}.py {args[2:]}')
            
            Modules[0].run(
                'run', args[1].title(), 
                'True', # VISIBLE
                ('-v' in args) # VERBOSE
            )

        #===========================================
        case 'args':
        # ARGS

            #===========================================
            if args[1] == 'service':
            # ARGS SERVICE #

                Services[int(args[2])].args = args[4:]

                print('Updated Arguements ...')

        #===========================================
        case 'check':
        # CHECK
            
            #===========================================
            if args[1] == 'service':
            # CHECK SERVICE

                for serv in mem['service']:

                    RUNNING: str = ('Running'  if serv.running else 'Stopped')
                    ENABLED: str = (' Enabled' if serv.enabled else 'Disabled')

                    print(f'{Services.index(serv)}: [{RUNNING}, {ENABLED}] {serv.path}')

            #===========================================

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

    except Exception as e:

        warn(e)

#===========================================================================