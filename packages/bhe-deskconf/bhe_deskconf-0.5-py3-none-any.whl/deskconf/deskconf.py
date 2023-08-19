from pathlib import Path
from attrib import Attrib
from shutil import copy

__info = "IdhinBhe OJO DI UTAK-ATIK SU......"


def syntax(icofilename,
           info=__info):
    shellsyntax = f"""[.ShellClassInfo]
ConfirmFileOp=0
NoSharing=1
IconFile={icofilename}
IconIndex=0
InfoTip={info}"""
    return shellsyntax


def __allsubdir(path=Path()):
    return [dir for dir in path.glob("**") if dir.is_dir()]


def __rename_looper(paths, ico_name="icon"):
    for folder in paths:
        for ico in folder.glob("*.ico"):
            try:
                ico.rename(folder / f"{ico_name}{ico.suffix}")
            except FileExistsError:
                pass


def renameall_ico(path=Path(), subfol=False, ico_name="icon"):
    """ Renaming all ico file in subfolder to "icon.ico"

    param:
    path(Path): Path Object"""

    if not subfol:
        __rename_looper(path.iterdir(), ico_name=ico_name)
    if subfol:
        __rename_looper(__allsubdir(path), ico_name=ico_name)


def __rmconf_looper(paths):
    for folder in paths:
        for conf in folder.glob("*.ini"):
            print(conf)
            Attrib(conf).unset_r
            Attrib(conf).unset_s
            Attrib(conf).unset_sh()
            conf.unlink()


def rmall_conf(path=Path(), subfol=False):
    """ Removing all desktop.ini in all child path

    param:
    path(Path): Path Object
    """
    if not subfol:
        __rmconf_looper(path.iterdir())
    if subfol:
        __rmconf_looper(__allsubdir(path))


def __set_looper(paths, info=__info):
    for folder in paths:
        for ico in folder.glob("*.ico"):
            desktop_conf = folder / "desktop.ini"
            print(f"creating 'desktop.ini' in {folder}")
            desktop_conf.write_text(syntax(ico.name, info=info))
            Attrib(folder).set_s()
            print(f"hiding {ico}")
            Attrib(ico).set_h()
            print(f"set system and hiding 'desktop.ini' in {folder}")
            Attrib(desktop_conf).set_sh()


def set_all(path=Path(), subfol=False, info=__info):
    """Setting up all desktop.ini, if in all subdir already have ico files

    1 - removing all config
    2 - renaming all ico files
    3 - creating desktop.ini

    param:
    path(Path): Path Object"""
    if not subfol:
        rmall_conf(path, subfol=False)
        renameall_ico(path, subfol=False)
        __set_looper(path.iterdir())
    if subfol:
        rmall_conf(path, subfol=True)
        renameall_ico(path, subfol=True)
        __set_looper(__allsubdir(path), info=info)


def __copy_looper(iterable_paths):
    folders = [folder for folder in iterable_paths if folder.is_dir()]
    try:
        for folder in folders:
            exist = [ico for ico in folder.glob(
                "*.ico") if ico.name == "icon.ico"]
            if not exist:
                copy(ico, f"{folder}\icon.ico")
                print(f"Copying {ico.name} to {folder} as 'icon.ico'")
            if exist:
                print(f"'icon.ico' already exist in {folder} -- Skipping.....")
    except PermissionError:
        pass


ico = [ico for ico in Path().glob("*.ico")][0]


def one_for_all(ico=ico, path=Path(), subfol=False, info=__info):
    """set one icon for all """
    if not subfol:
        __copy_looper(path.iterdir())
        set_all(path, info=info)
    if subfol:
        __copy_looper(__allsubdir(path))
        set_all(path, info=info, subfol=True)
