from ...Items import Services, Modules, HardDrives, PCIeCards, VirtualDisks, Towers

class Branch:

    def __init__(self,
        *args: str
    ) -> None:

        # If no args passed
        if len(args) == 0:
            self._NoArgs()

        # If command does not exist
        elif not hasattr(self, args[0]):
            print()
            print(f'INVALID COMMAND')
            print("Type 'help' for a list of commands")
            print()

        else:

            # Run Command
            getattr(self, args[0]) (*args[1:])

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

    def RunFile(
        path: str,
        args: tuple = ()
    ) -> None:
        print(f'Running: {path} {args}')

    def Error(
        name: str,
        mess: str = ''
    ) -> None:        
        print(f'<{name}> {mess}')
