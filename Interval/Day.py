from . import IS_SERVER, main_repo

if IS_SERVER:

    main_repo.reset()

    main_repo.add('/Minecraft/Worlds/')
    main_repo.add('/Plex/Plex Media Server/Plug-in Support/Databases/')

    if main_repo.changes > 0:

        new_commit = main_repo.commit(
            message = f"Automated Backup",
            skip_hooks = True,
        )

        main_repo.push()
