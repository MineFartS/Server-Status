from philh_myftp_biz.modules import Module, Service
from ...Items import Services, Modules

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

    services: list[Service] = Services.copy()

    modules: list[Module] = Modules.copy()

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
