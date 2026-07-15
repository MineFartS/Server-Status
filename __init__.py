from subprocess import run
from sys import executable

def pip(*args) -> None:
    run([executable, '-m', 'pip', *args])

