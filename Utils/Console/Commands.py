from .Types import NestedCommand

class CommandTree(NestedCommand):

    from builtins import exit

    @staticmethod
    def cls() -> None:
        from philh_myftp_biz.terminal import cls
        
        cls()

        print(f"""
|---------------------------|
       Phil's Server
     [philh.myftp.biz]

    MANAGEMENT  CONSOLE
|---------------------------|

Type 'help' for a list of commands
""")

    class help(NestedCommand):

        def _NI(self, *_) -> None:

            print("""
----------------------------------------

CLS     | Clear the terminal
EXIT    | Exit the terminal

RUN     | Run a script

LIST    | List items
SELECT  | Select items
START   | Start items
STOP    | Stop items
CHECK   | Get items' status
ENABLE  | Enable items
DISABLE | Disable items
ARGS    | Set items' arguements

----------------------------------------

Run 'help *cmd*' for more details about a specific command

----------------------------------------
""")

        list = lambda _: print("""
LIST SERVICE      | Get a list of selected services
LIST MODULE       | Get a list of selected modules
""")
            
        select = lambda _: print("""
SELECT SERVICE [#|#..|..#|#..#|#,#] | Select services (Ex: select service 1,3)
SELECT MODULE  [#|#..|..#|#..#|#,#] | Select modules (Ex: select module ..5)
""")
            
        start = lambda _: print("""
START SERVICE | Start the selected services
""")
    
        stop = lambda _: print("""
STOP SERVICE | Stop the selected services
""")

        check = lambda _: print("""
CHECK SERVICE | Get the status of the selected services
""")
            
        enable = lambda _: print("""
ENABLE SERVICE | Enable the selected services
""")
            
        disable = lambda _: print("""
DISABLE SERVICE | Disable the selected services
""")
            
        run = lambda _: print("""
RUN *SCRIPT*    | Run a script in a new tab (Ex: run Interval.Startup)
RUN *SCRIPT* -v | Run a script in a new tab [VERBOSE] (Ex: run Interval.Startup -v)

SCRIPTS:
    - Utils.Setup
    - Utils.Update
    - Utils.Status
    - Utils.Console
    - Interval.Day
    - Interval.Hour
    - Interval.Week
    - Interval.Startup
""")
            
        args = lambda _: print("""
ARGS SERVICE = *arg1* *arg2* ...   | Set the args for selected services
""")

    def run(self, 
        script: str,
        *args: str
    ) -> None:
        from ...Items import Modules

        print(f'Running: C:/Scripts/{script.replace('.', '/')}.py {args}')
        
        Modules[0].run(
            'run', script.title(), 
            'True', # VISIBLE
            ('-v' in args) # VERBOSE
        )

#===========================================================================
'''
def run(*args:str) -> None:

    match args[0]:
   
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
        case 'args':
        # ARGS

            #===========================================
            if args[1] == 'service':
            # ARGS SERVICE

                print('Updating Arguements for Selected Services ...')

                services: list[Service] = mem['service']

                for serv in services:

                    serv.args = args[4:]

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

'''