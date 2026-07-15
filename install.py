from . import pip

try:
    import philh_myftp_biz, pybind11_stubgen, wmi # pyright: ignore[reportUnusedImport]

except ModuleNotFoundError:

    pip('install', '-U', 'git+https://github.com/MineFartS/Server-PythonPackage.git')
    from philh_myftp_biz.modules import Module

    #=================================================================================
    # Install this Module

    pip('install', 'pybind11-stubgen')
    pip('install', 'wmi')

    #=================================================================================
    # Add Scheduled Tasks
    
    this = Module('C:/Scripts/')

    this.run('xml/set', 'Startup')
    this.run('xml/set', 'Hour')
    this.run('xml/set', 'Week')

    #=================================================================================

