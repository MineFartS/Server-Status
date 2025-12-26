from Status_Items.Services import Services
from philh_myftp_biz.terminal import cls
from shlex import split

# Loop Forever
while True:

    # Ask for and process user input
    raw = input(f'\\> ').lower()
    args = split(raw)

    # Exit terminal if certain command given
    if args[0] in ['quit', 'exit', 'close', 'stop', 'end', 'leave']:
        exit()

    elif args[0] in ['cls', 'clear']:
        cls()

    else:

        for s in Services:

            if s.name.lower() == args[0]:

                for a in dir(s):

                    if a.lower() == args[1]:

                        out = getattr(s, a)

                        if callable(out):

                            out = out()

                        if out != None:
                            print(out)

                        break
