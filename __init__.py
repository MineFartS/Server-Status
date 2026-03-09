
# Run 'Setup.py' if philh_myftp_biz is not installed
try:    
    import philh_myftp_biz # pyright: ignore[reportUnusedImport]
except ModuleNotFoundError:
    from . import Setup # pyright: ignore[reportUnusedImport]
