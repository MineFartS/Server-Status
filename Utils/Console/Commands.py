from .Types import Branch, Memory, Printer

class Tree(Branch):

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

    class help(Branch):

        @staticmethod
        def _NoArgs() -> None:
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

        def __getattribute__(self, name:str):
        
            value = super().__getattribute__(name)

            if isinstance(value, str):
                return lambda: print(value)
            else:
                return value

        list = """
LIST SERVICE      | Get a list of selected services
LIST MODULE       | Get a list of selected modules
"""
            
        select = """
SELECT SERVICE [...] | Select services (Ex: select service 1,3)
SELECT MODULE  [...] | Select modules (Ex: select module ..5)

[...] -> ['#', '#..', '..#', '#..#', '#,#']
"""
            
        start = """
START SERVICE | Start the selected services
"""
    
        stop = """
STOP SERVICE | Stop the selected services
"""

        check = """
CHECK SERVICE | Get the status of the selected services
"""
            
        enable = """
ENABLE SERVICE | Enable the selected services
"""
            
        disable = """
DISABLE SERVICE | Disable the selected services
"""
            
        run = """
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
"""
            
        args = """
ARGS SERVICE = *arg1* *arg2* ...   | Set the args for selected services
"""

    @staticmethod
    def run( 
        script: str,
        *args: str
    ) -> None:
        from ...Items import Modules

        Printer.RunFile(
            path = f"C:/Scripts/{script.replace('.', '/')}.py",
            args = args
        )
        
        Modules[0].run(
            'run', script.title(), 
            'True', # VISIBLE
            ('-v' in args) # VERBOSE
        )

    class list(Branch):

        @staticmethod
        def service() -> None:
            from ...Items import Services

            for serv in Memory.services:
                    
                print(f'{Services.index(serv)}: {serv.path} {serv.args}')

        @staticmethod
        def module() -> None:
            from ...Items import Modules

            for mod in Memory.modules:
                    
                print(f'{Modules.index(mod)}: {mod.path}')

    class select(Branch):

        @staticmethod
        def service(rslice:str) -> None:
            from philh_myftp_biz.text import to_slice
            from ...Items import Services

            Memory.services = []

            for slice in to_slice(rslice):

                _serv = Services[slice]

                if isinstance(_serv, list):
                    Memory.services += _serv
                else:
                    Memory.services += [_serv]
                 
            Tree.list.service()

        @staticmethod
        def module(rslice:str) -> None:
            from philh_myftp_biz.text import to_slice
            from ...Items import Modules

            Memory.modules = []

            for slice in to_slice(rslice):

                _mod = Modules[slice]

                if isinstance(_mod, list):
                    Memory.modules += _mod
                else:
                    Memory.modules += [_mod]
                 
            Tree.list.module()

    class start(Branch):

        @staticmethod
        def service() -> None:
            
            for serv in Memory.services:

                if serv.exists:

                    Printer.RunFile(
                        path = serv.file('Start'),
                        args = serv.args
                    )

                    serv.start(force=True)

                else:
                    Printer.Error('ServiceMissing', serv)

    class check(Branch):

        @staticmethod
        def service() -> None:
            from ...Items import Services

            for serv in Memory.services:

                RUNNING: str = ('Running'  if serv.running else 'Stopped')
                ENABLED: str = (' Enabled' if serv.enabled else 'Disabled')

                print(f'{Services.index(serv)}: [{RUNNING}, {ENABLED}] {serv.path}')

    class stop(Branch):

        @staticmethod
        def service() -> None:

            for serv in Memory.services:

                if serv.exists:

                    Printer.RunFile(
                        path = serv.file('Stop')
                    )

                    serv.stop()

                else:
                    Printer.Error('ServiceMissing', serv)

    class enable(Branch):

        @staticmethod
        def service() -> None:

            for serv in Memory.services:

                serv.enable()

            Tree.check.service()

    class disable(Branch):

        @staticmethod
        def service() -> None:

            for serv in Memory.services:

                serv.disable()

            Tree.check.service()

    class args(Branch):

        @staticmethod
        def service(_, *args:str) -> None:

            for serv in Memory.services:

                serv.args = args

            Tree.list.service()

#===========================================================================
