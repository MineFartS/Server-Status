from .Types import Branch, Memory, Printer

# TODO Add leading 0 to list, check, etc.

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

        def __getattribute__(self, name:str):
        
            value = super().__getattribute__(name)

            if isinstance(value, str):
                return lambda: print(value)
            else:
                return value

        _NoArgs = """
----------------------------------------

HELP    | Show help message
CLS     | Clear the terminal
EXIT    | Exit the terminal

RUN     | Run a script

NAME    | Get Computer Name
IP      | Get IP Address

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
"""

        list = """
LIST SERVICE      | Get a list of selected services
LIST MODULE       | Get a list of selected modules
LIST DISK         | Get a list of selected hard drives
LIST VDISK        | Get a list of selected virtual disks
LIST PCIE         | Get a list of selected pcie cards
LIST TOWER        | Get a list of selected towers
"""
            
        select = """
SELECT SERVICE [...] | Select services (Ex: select service 1,3)
SELECT MODULE  [...] | Select modules (Ex: select module ..5)
SELECT DISK    [...] | Select hard drives
SELECT VDISK   [...] | Select virtual disks
SELECT PCIE    [...] | Select pcie cards
SELECT TOWER   [...] | Select towers

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
CHECK MODULE  | Get the status of the selected modules
CHECK DISK    | Get the status of the selected hard drives
CHECK VDISK   | Get the status of the selected virtual disks
CHECK PCIE    | Get the status of the selected pcie cards
CHECK TOWER   | Get the status of the selected towers
"""
            
        enable = """
ENABLE SERVICE | Enable the selected services
ENABLE MODULE  | Setup dependencies for the selected modules
"""
            
        disable = """
DISABLE SERVICE | Disable the selected services
"""
            
        run = """
RUN *SCRIPT*    | Run a script in a new tab (Ex: run Interval.Startup)
RUN *SCRIPT* -v | Run a script in a new tab [VERBOSE] (Ex: run Interval.Startup -v)

SCRIPTS:
    - Utils.Update
    - Utils.Status
    - Utils.Console
    - Interval.Hour
    - Interval.Week
    - Interval.Startup
"""
            
        args = """
ARGS SERVICE = *arg1* *arg2* ...   | Set the args for selected services
"""

        name = """
NAME   | Get the name of the current computer
"""

        ip = """
IP LAN | Get the current local ip
IP WAN | Get the current public ip
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
        def _hardware(
            src: list,
            mem: list
        ) -> None:
            for dev in mem:  
                print(f'{src.index(dev)}: {dev.Name}')

        @staticmethod
        def service() -> None:
            from ...Items import Services

            for serv in Memory.Services:
                    
                print(f'{Services.index(serv)}: {serv.path} {serv.args}')

        @staticmethod
        def module() -> None:
            from ...Items import Modules

            for mod in Memory.Modules:
                    
                print(f'{Modules.index(mod)}: {mod.path}')

        @staticmethod
        def disk() -> None:
            from ...Items import HardDrives

            Tree.list._hardware(
                src = HardDrives,
                mem = Memory.Disks
            )

        @staticmethod
        def pcie() -> None:
            from ...Items import PCIeCards

            Tree.list._hardware(
                src = PCIeCards,
                mem = Memory.PCIeCards
            )

        @staticmethod
        def vdisk() -> None:
            from ...Items import VirtualDisks

            Tree.list._hardware(
                src = VirtualDisks,
                mem = Memory.VDisks
            )

        @staticmethod
        def tower() -> None:
            from ...Items import Towers

            Tree.list._hardware(
                src = Towers,
                mem = Memory.Towers
            )

    class select(Branch):

        @staticmethod
        def _all(
            rslice: str, 
            src: list, 
            dst: list
        ) -> None:
            from philh_myftp_biz.text import to_slice

            dst.clear()

            for slice in to_slice(rslice):

                _mod = src[slice]

                if isinstance(_mod, list):
                    dst += _mod
                else:
                    dst += [_mod]

        @staticmethod
        def service(rslice:str) -> None:
            from ...Items import Services

            Tree.select._all(
                rslice = rslice,
                src = Services,
                dst = Memory.Services
            )
                 
            Tree.list.service()

        @staticmethod
        def module(rslice:str) -> None:
            from ...Items import Modules

            Tree.select._all(
                rslice = rslice,
                src = Modules,
                dst = Memory.Modules
            )
                 
            Tree.list.module()

        @staticmethod
        def disk(rslice:str) -> None:
            from ...Items import HardDrives

            Tree.select._all(
                rslice = rslice,
                src = HardDrives,
                dst = Memory.Disks
            )
                 
            Tree.list.disk()

        @staticmethod
        def pcie(rslice:str) -> None:
            from ...Items import PCIeCards

            Tree.select._all(
                rslice = rslice,
                src = PCIeCards,
                dst = Memory.PCIeCards
            )
                 
            Tree.list.pcie()

        @staticmethod
        def vdisk(rslice:str) -> None:
            from ...Items import VirtualDisks

            Tree.select._all(
                rslice = rslice,
                src = VirtualDisks,
                dst = Memory.VDisks
            )
                 
            Tree.list.vdisk()

        @staticmethod
        def tower(rslice:str) -> None:
            from ...Items import Towers

            Tree.select._all(
                rslice = rslice,
                src = Towers,
                dst = Memory.Towers
            )
                 
            Tree.list.tower()

    class start(Branch):

        @staticmethod
        def service() -> None:
            
            for serv in Memory.Services:

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
        def _hardware(
            src: list,
            mem: list
        ) -> None:

            for dev in mem:

                ACTIVE: str = (' Active ' if dev.Connected else 'Inactive')

                print(f'{src.index(dev)}: [{ACTIVE}] {dev.Name}')

        @staticmethod
        def service() -> None:
            from ...Items import Services

            for serv in Memory.Services:

                RUNNING: str = ('Running'  if serv.running else 'Stopped')
                ENABLED: str = (' Enabled' if serv.enabled else 'Disabled')

                print(f'{Services.index(serv)}: [{RUNNING}, {ENABLED}] {serv.path}')

        @staticmethod
        def module() -> None:
            from ...Items import Modules

            for mod in Memory.Modules:

                EXISTS: str = (' Exists' if mod.exists else 'Missing')

                print(f'{Modules.index(mod)}: [{EXISTS}] {mod.path}')

        @staticmethod
        def disk() -> None:
            from ...Items import HardDrives

            Tree.check._hardware(
                src = HardDrives,
                mem = Memory.Disks
            )

        @staticmethod
        def pcie() -> None:
            from ...Items import PCIeCards

            Tree.check._hardware(
                src = PCIeCards,
                mem = Memory.PCIeCards
            )

        @staticmethod
        def tower() -> None:
            from ...Items import Towers

            Tree.check._hardware(
                src = Towers,
                mem = Memory.Towers
            )

    class stop(Branch):

        @staticmethod
        def service() -> None:

            for serv in Memory.Services:

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

            for serv in Memory.Services:

                serv.enable()

            Tree.check.service()

        @staticmethod
        def module() -> None:

            for mod in Memory.Modules:

                print(f'Enabling: {mod}')
                
                mod.install(False)

    class disable(Branch):

        @staticmethod
        def service() -> None:

            for serv in Memory.Services:

                serv.disable()

            Tree.check.service()

    class args(Branch):

        @staticmethod
        def service(_, *args:str) -> None:

            for serv in Memory.Services:

                serv.args = args

            Tree.list.service()

    @staticmethod
    def name() -> None:
        from philh_myftp_biz.pc import NAME

        print(f'\nPC Name: {NAME}')

    class ip(Branch):

        @staticmethod
        def lan() -> None:
            from philh_myftp_biz.web import IP

            print(f'\nLocal IP: {IP.LAN}')

        @staticmethod
        def wan() -> None:
            from philh_myftp_biz.web import IP

            print(f'\nPublic IP: {IP.WAN}')

#===========================================================================
