
# Run 'Setup.py' if philh_myftp_biz is not installed
try:    
    import philh_myftp_biz # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError:
    
    #=================================================================================
    # PHILH_MYFTP_BIZ PKG

    from subprocess import run
    from sys import executable

    run([
        executable, '-m', 'pip', 
        'install', 'git+https://github.com/MineFartS/Server-PythonPackage.git'
    ])


    from .Items import Modules

    #=================================================================================
    # Add Scheduled Tasks

    Modules[0].run('xml/set', 'Startup')
    Modules[0].run('xml/set', 'Hour')
    Modules[0].run('xml/set', 'Week')

    #=================================================================================
    # INSTALL MODULES

    for m in Modules:
        
        m.install()

    #=================================================================================
