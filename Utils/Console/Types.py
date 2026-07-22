from ...Items import Services, Modules, HardDrives, PCIeCards, VirtualDisks, Towers
from philh_myftp_biz.functools import force_types

class Branch:

    def __init__(self,
        *args: str
    ) -> None:

        # If no args passed
        if len(args) == 0:
            self._NoArgs()

        # If command does not exist
        elif not hasattr(self, args[0].lower()):
            print()
            print(f'INVALID COMMAND')
            print("Type 'help' for a list of commands")
            print()

        else:

            # Run Command
            getattr(self, args[0].lower()) (*args[1:])

    @staticmethod
    def _NoArgs() -> None:
        Printer.Error('NoArgs', 'This command requires arguements')

class Memory:

    Services= Services.copy()

    Modules= Modules.copy()

    Disks = HardDrives.copy()

    PCIeCards = PCIeCards.copy()

    VDisks = VirtualDisks.copy()

    Towers = Towers.copy()

class Printer:

    @force_types
    def RunFile(
        path: str,
        args: tuple = ()
    ) -> None:
        print(f'Running: {path} {args}')

    @force_types
    def Error(
        name: str,
        mess: str = ''
    ) -> None:        
        print(f'<{name}> {mess}')
