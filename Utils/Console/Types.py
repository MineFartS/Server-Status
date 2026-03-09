
class NestedCommand:

    def __init__(self, 
        name: str = '',
        *args: str
    ) -> None:
        from philh_myftp_biz.classtools import attrs

        for attr in attrs(self):

            if attr.name == name:

                attr.value(*args)

                break

        else:
            self._NI(*args)                    

    def _NI(self, cmd:str, *_) -> None:

        print(f"""
"{cmd}" NOT IMPLEMENTED

Type 'help' for a list of commands
""")
