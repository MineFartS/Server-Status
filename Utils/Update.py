from subprocess import run
from sys import executable

run([
    executable, '-m', 'pip', 
    'install', 'git+https://github.com/MineFartS/Server-PythonPackage.git'
])
