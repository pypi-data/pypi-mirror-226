#! /usr/bin/python3

from typing import Tuple, List, Union, Dict, Optional, Any
from dataclasses import dataclass
import sys
from pathlib import Path
import shlex
from subprocess import Popen, PIPE
import argparse
import logging

import yaml


T_Path = Union[str, Path]
T_Dir_Dict = Dict[str, Dict[str, Any]]


@dataclass
class Config:
    host: Optional[str] = None
    root: Optional[str] = None
    logfile: Optional[str] = None
    dirs: Optional[T_Dir_Dict] = None
    exclusions: Optional[List] = None


def check_host_given(args: argparse.Namespace, host: Optional[str]) -> str:
    """Check if the given host is online.

    :code:`args.host` overrides :code:`host`. See :func:`check_host` for details
    of how it's checked

    Args:
        args: Namespace of commandline arguments
        host: Any other host specified via config

    """
    logger = logging.getLogger("backup-rsync")
    host = args.host or host    # override host if given in args
    if not host:
        logger.error("No host found from config or command line arguments")
        sys.exit(1)
    if not check_host(host) and not args.print_only:
        logger.error(f"Host {host} not reachable")
        sys.exit(1)
    return host


def check_host(host: str, port: int = 22) -> bool:
    """Check if a given host:port combination is online

    Uses :code:`nc` process to perform the check.

    Args:
        host: name or addr of host
        port: port to check

    Example:
        >>> check_host("localhost", 22)
        True

        >>> check_host("localhost", 23)
        False

    """
    if "@" in host:
        host = host.split("@")[1]
    logger = logging.getLogger("backup-rsync")
    p = Popen(shlex.split(f"nc -z -v {host} {port}"), stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(timeout=1)
    output = err.decode("utf-8").lower()
    if "sent" in output and "received" in output:
        return True
    elif "no route" in output:
        return False
    elif "connection refused" in output:
        return False
    else:
        logger.error(f"Unknown output {output}")
        return False


def check_root_path(args: argparse.Namespace, root_path: Optional[str]):
    """Check if the root path in args or given root_path exists

    Args:
        args: Namespace of commandline arguments
        root_path: Root path in config

    """
    logger = logging.getLogger("backup-rsync")
    root_path = args.root_path or root_path
    if not root_path:
        logger.error("Root path could not be determined. Check config or give at command line")
        sys.exit(1)
    if not Path(root_path).exists():
        logger.error("Root path doesn't exist")
        sys.exit(1)
    return root_path


def check_dirs_all(args: argparse.Namespace, dirs: T_Dir_Dict) -> T_Dir_Dict:
    """Check directories read from configuration file for backup

    Args:
        args: Command line arguments
        dirs: Dictionary of directories and flags

    """
    logger = logging.getLogger("backup-rsync")
    if not dirs:
        logger.error("Cannot backup \"all\" if no configured dirs in file")
        sys.exit(1)
    if args.exclude_with_subdirs:
        dirs = {k: v for k, v in dirs.items() if not v.get("subdirs", False)}
    else:
        dirs = dirs
    return dirs


def check_dirs_given(args: argparse.Namespace, dirs: Optional[T_Dir_Dict]) -> T_Dir_Dict:
    """Check given directories for backup

    Args:
        args: Command line arguments
        dirs: Dictionary of directories and flags


    If directories are given, check for flags in config. In case :code:`dirs` are not in
    config check appropriate switches and set backup options.

    """
    logger = logging.getLogger("backup-rsync")
    # dirs = cond([(not args.unconfigured and dirs,
    #               {d: dirs[d] for d in args.dirs.split(",")
    #                if d in dirs}),
    #              (not args.force)])
    if not dirs:
        unconfigured_dirs = args.dirs.split(",")
    else:
        unconfigured_dirs = set(map(str.strip, args.dirs.split(","))) - dirs.keys()
    if args.diff:
        dirs = {d: {"delete": args.delete} for d in args.dirs.split(",")}
    elif not args.unconfigured and dirs:
        if unconfigured_dirs:
            logger.error(f"Need \"--allow-unconfigured\" with unconfigured directories {args.dirs}")
            sys.exit(1)
        dirs = {d: dirs[d] for d in args.dirs.split(",")
                if d in dirs}
    else:
        if unconfigured_dirs and len(args.dirs.split(",")) > len(unconfigured_dirs):
            logger.error(f"Configured dirs {set(args.dirs.split(',')) - unconfigured_dirs}"
                         " cannot be backed up with unconfigured")
            sys.exit(1)
        if args.unconfigured and not unconfigured_dirs:
            logger.error("Backup for unconfigured dirs given but no unconfigured dirs")
            sys.exit(1)
        if not args.force:
            dirs = {d: {"delete": False} for d in args.dirs.split(",")}
            args.dry_run = True
            logger.info(f"Only doing DRY RUN with delete=False on unconfigured {[*dirs.keys()]}. " +
                        "Set \"--force\" and \"--delete\" respectively if this is not what you want.")
        else:
            dirs = {d: {"delete": args.delete} for d in args.dirs.split(",")}
    return dirs


def check_dirs(args: argparse.Namespace, configured_dirs: Optional[T_Dir_Dict]) -> T_Dir_Dict:
    """Check and update the flags for directories.

    Args:
        args: Command line arguments
        configured_dirs: Dictionary of directories and flags

    The dirs given at command line may be one of \"all\" or as a comma separated list.

    """
    logger = logging.getLogger("backup-rsync")
    if not args.dirs:
        logger.error("Directories to backup must be specified")
        sys.exit(1)
    splits = args.dirs.split(",")
    if "all" in splits and len(splits) > 1:
        logger.error("\"all\" cannot be given with any other directories")
        sys.exit(1)
    elif args.dirs == "all":
        if not configured_dirs:
            logger.error("Dirs \"all\" given, but nothing is configured in config file")
            sys.exit(1)
        dirs = check_dirs_all(args, configured_dirs)
    else:
        dirs = check_dirs_given(args, configured_dirs)
        if len(splits) > len(dirs):
            logger.error(f"Configured dirs {[*dirs.keys()]} cannot be backed up with unconfigured "
                         f"{set(splits) - dirs.keys()}")
            sys.exit(1)
    return dirs


# TODO: add individual delete flag for dirs? Maybe?
def check_delete_flag(args: argparse.Namespace, dirs: T_Dir_Dict):
    """Check and update the delete flag for directories.

    Args:
        args: Command line arguments
        dirs: Dictionary of directories and flags


    """
    logger = logging.getLogger("backup-rsync")
    if args.no_delete:
        for k, v in dirs.items():
            v.update({"delete": False})
    if args.delete and dirs:
        if not args.force and not args.diff:
            logger.error("Need \"--force\" to override \"--delete\" for configured directories")
            sys.exit(1)
        else:
            for k, v in dirs.items():
                v.update({"delete": True})


def run_cmd(cmd: List[str]) -> Tuple[str, str]:
    """Run a command `cmd`, capture stdout and stderr and return them as strings

    Args:
        cmd: The shell command

    """
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.decode("utf-8"), err.decode("utf-8")


def rsync_subr(user_host: str, dir_a: T_Path, dir_b: Optional[T_Path] = None,
               from_remote: bool = False, delete: bool = False,
               extra_args: list = [],
               dry_run: bool = False, print_only: bool = False):
    """Subroutine that actually calls `rsync`

    Args:
        user_host: user@host string
        dir_a: Source directory
        dir_b: target directory
        from_remote: If True then copy from the host instead of copying to the host
        delete: `--delete` flag of `rsync`
        dry_run: `--dry-run` flag of `rsync`
        print_only: Only print the `rsync` command. Don't actually do anything.
                    Not even dry run.


    """
    logger = logging.getLogger("backup-rsync")
    if not dir_b:
        dir_b = dir_a
    dir_a = str(Path(dir_a).absolute())
    dir_b = str(Path(dir_b).absolute())
    if not dir_a.endswith("/"):
        dir_a += "/"
    if not dir_b.endswith("/"):
        dir_b += "/"
        if from_remote:
            msg = f"Backing up {user_host}:{dir_b} to {dir_a}."
        else:
            msg = f"Backing up {dir_a} to {user_host}:{dir_b}."
    if delete:
        msg += " Deleting also."
    else:
        msg += " Not deleting"
    logger.info(msg)
    if dry_run:
        logger.info("DRY RUN")
    delete = "--delete" if delete else ""  # type: ignore
    dry_run = "n" if dry_run else ""       # type: ignore
    if from_remote:
        dir_order = f"{user_host}:{dir_b} {dir_a}"
    else:
        dir_order = f"{dir_a} {user_host}:{dir_b}"
    cmd = f"rsync -auxv{dry_run} {delete} -e ssh {dir_order} " +\
        (" ".join(extra_args) if extra_args else "")
    if print_only:
        logger.info(cmd)
        return "", ""
    else:
        return run_cmd(shlex.split(cmd))


def rsync_over_ssh(user_host: str, dir_a: T_Path, dir_b: Optional[T_Path] = None,
                   delete: bool = False, subdirs: bool = False,
                   from_remote: bool = False, diff: bool = False,
                   extra_args: list = [],
                   dry_run: bool = False, print_only: bool = False) ->\
                   Tuple[Union[str, dict], Union[str, dict]]:
    """Rsync over `ssh` from `dir_a` to `dir_b`

    Args:
        user_host: user@host
        dir_a: source directory
        dir_b: target directory. If None the same path on target machine is the target
               directory
        delete: Delete also. Equivalent to passing --delete to `rsync`
        subdirs: Instead of source directory, `rsync` each subdirectory in source
                 directory individually. Useful in case the source directory has fewer
                 subdirectories than target and you don't want to overwrite or delete them.
        dry_run: Dry run. Equivalent of option `--dry-run` of `rsync`
        print_only: Only print the rsync command, don't actually do anything.

    """
    logger = logging.getLogger("backup-rsync")
    if diff:
        dry_run = True
    if subdirs:
        out = {}
        err = {}
        if dir_b is not None:
            raise ValueError("Target directory cannot be given with subdirectories")
        for dir in Path(dir_a).iterdir():
            out[str(dir)], err[str(dir)] = rsync_subr(user_host, dir,
                                                      from_remote=from_remote,
                                                      delete=delete,
                                                      extra_args=extra_args,
                                                      dry_run=dry_run,
                                                      print_only=print_only)
            if not print_only:
                logger.debug(out[str(dir)])
            splits = out[str(dir)].split("\n")
            target_dir = f"{user_host}:{dir_b or dir_a}"
            if from_remote:
                logger.info(f"From {target_dir} to {dir_a}")
            else:
                logger.info(f"From {dir_a} to {target_dir}")
            if not print_only:
                logger.info(splits[-3])
                logger.info(splits[-2])
            if err[str(dir)]:
                logger.error(err[str(dir)])
    else:
        out, err = rsync_subr(user_host, dir_a, dir_b=dir_b,
                              from_remote=from_remote,
                              delete=delete,
                              extra_args=extra_args,
                              dry_run=dry_run,
                              print_only=print_only)
        if out:
            if diff:
                logger.info(out)
            else:
                logger.debug(out)
            splits = str(out).split("\n")
            target_dir = f"{user_host}:{dir_b or dir_a}"
            if from_remote:
                logger.info(f"From {target_dir} to {dir_a}")
            else:
                logger.info(f"From {dir_a} to {target_dir}")
            if not print_only:
                logger.info(splits[-3])
                logger.info(splits[-2])
        if err:
            logger.error(err)
    return out, err


def create_logger(logfile: Optional[Path], verbosity: str) -> None:
    """Create a logger with a given verbosity

    Args:
        logfile: path to logfile
        verbosity: Verbosity of the stream handler

    The verbosity (level) of the logger and the file handler is always DEBUG


    """
    logger = logging.getLogger("backup-rsync")
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    level = getattr(logging, verbosity.upper())
    stream_handler.setLevel(level)
    if logfile:
        file_formatter = logging.Formatter(datefmt='%Y/%m/%d %I:%M:%S %p',
                                           fmt="[%(asctime)s] [%(levelname)s] %(message)s")
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
    stream_formatter = logging.Formatter(fmt="[%(levelname)s] %(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)



def read_config(config_file: Path) -> Config:
    """Read a yaml config file

    Args:
        config_file: Path to config file


    """
    if config_file.exists():
        with open(Path.home().joinpath(".rsync-backup")) as f:
            config = Config(**yaml.load(f, Loader=yaml.FullLoader))
    else:
        config = Config(**{})
    return config


def list_and_exit(configured_dirs: Optional[Dict[str, Any]]) -> None:
    """List the supported directories or raise error

    Args:
        configured_dirs: Dictionary of dirs and options


    """
    logger = logging.getLogger("backup-rsync")
    if configured_dirs:
        print(yaml.dump(configured_dirs))
        sys.exit(0)
    else:
        logger.error("No supported dirs in config")
        sys.exit(1)


def main() -> int:
    default_config_file = Path.home().joinpath(".rsync-backup")
    usage = """\tSimple script to manage backup of similar directory structures across hosts.

\tThe directories to backup can be read from a config file and the required
\tdirectories can be backed up.

\tAdditional flags that are supported are:
\t    subdirs: [True, False]
\t    delete: [True, False]

\tThe :code:`subdirs` flag implies that instead of syncing the directory to remote, only
\tbackup those subdirectories /under/ the given directory which /already exist/ on
\tremote. In effect new directories are not created.

\t:code:`delete` simply passes on the --delete flag to :code:`rsync`

"""
    parser = argparse.ArgumentParser("Rsync backup tool",
                                     usage=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--dirs", default="", help="Comma separated list of directories to backup")
    parser.add_argument("--targets", default="", help="Comma separated list of target directories")
    parser.add_argument("--list", action="store_true",
                        help="List the supported/configured directories in configuration and exit.")
    parser.add_argument("--exclude-with-subdirs", action="store_true",
                        help="Do not backup any directory which has \"subdirs\" attribute.")
    parser.add_argument("--exclude-subdirs", type=str,
                        help="Exclude these subdirs from all directories where subdir parameter is true.")
    parser.add_argument("--force", action="store_true",
                        help="Force allow --delete option on unconfigured directories")
    parser.add_argument("--delete", action="store_true",
                        help="Allow --delete option on unconfigured directories")
    parser.add_argument("--no-delete", action="store_true",
                        help="Do not delete even if given in config")
    parser.add_argument("--exclude", type=str, default="",
                        help="Exclude giver comma separated strings."
                        " These exclusions are appended to any given in the config.")
    parser.add_argument("--exclude-dirs", type=str, default="",
                        help="Exclude comma separated list of given directories if \"all\" is given.")
    parser.add_argument("--host", help="Remote host to backup")
    parser.add_argument("--check-host", help="Only check host. Don't do anything else",
                        action="store_true")
    parser.add_argument("-u", "--allow-unconfigured", dest="unconfigured", action="store_true",
                        help="Run on directories which are not configured."
                        " Use --list to see currently configured directories")
    parser.add_argument("--root", dest="root_path", default=Path.home(), type=Path,
                        help="Root path from which to consider directories for backup.")
    parser.add_argument("--diff", action="store_true",
                        help="Show only list of files to be updated.")
    parser.add_argument("--from", dest="from_remote", action="store_true",
                        help="Sync from the remote host instead of to.")
    parser.add_argument("--logfile", help="Log file for backup")
    parser.add_argument("--print-only", action="store_true",
                        help="Print the rsync command. Don't do anything not even dry-run.")
    parser.add_argument("--dry-run", action="store_true", help="Dry run.")
    parser.add_argument("-v", "--verbosity", choices=["info", "debug", "warning", "error"],
                        default="info", help="stdout verbosity")
    parser.add_argument("-c", "--config-file", default=default_config_file,
                        type=Path, help="Path to yaml configuration file." +
                        " Defaults to $HOME/.rsync_backup")
    args = parser.parse_args()

    config = read_config(args.config_file)
    configured_dirs = config.dirs
    if (config and config.logfile) or args.logfile:
        logfile = Path((config and config.logfile) or args.logfile)
        create_logger(logfile, verbosity=args.verbosity)
    else:
        create_logger(None, args.verbosity)
    logger = logging.getLogger("backup-rsync")
    if args.list:
        list_and_exit(configured_dirs)

    host = check_host_given(args, config.host)
    if args.check_host:
        logger.info(f"Host {host} is online")
        sys.exit(0)
    root_path = check_root_path(args, config.root)
    dirs = check_dirs(args, configured_dirs)

    extra_args = []
    if config.exclusions:
        extra_args.append(" ".join([f"--exclude='{e}'" for e in config.exclusions]))
    if args.exclude:
        extra_args.append(" ".join([f"--exclude='{e}'" for e in args.exclude.split(",")]))
    if args.dirs != "all" and args.exclude_dirs:
        logger.error("Specific dirs with --exclude-dirs cannot be given")
        sys.exit(1)
    if args.dirs == "all":
        exclude_dirs = args.exclude_dirs.split(",")
        for d in exclude_dirs:
            dirs.pop(d)
    targets = args.targets and args.targets.split(",")
    check_delete_flag(args, dirs)
    i = 0
    # TODO: The implementation is incorrect
    #       There's a separate subroutine for directories with `subdirs` flag
    #       where they're backed up in a loop.
    #       1. The correct version should flatten all the directories in a list,
    #          and pass them to rsync_over_ssh
    #       2. Also, then exclude_dirs option can be included after subdirs if required
    #          as right now, all subdirs are backed up
    #       3. Then it can be passed to command line args
    for dir, val in dirs.items():
        target = None if not targets else targets[i]
        out, err = rsync_over_ssh(host, root_path.joinpath(dir),
                                  dir_b=target,
                                  delete=val["delete"],
                                  subdirs=val.get("subdirs", False),
                                  from_remote=args.from_remote,
                                  diff=args.diff,
                                  extra_args=extra_args,
                                  dry_run=args.dry_run,
                                  print_only=args.print_only)
        if isinstance(err, dict):
            errs_to_log = {k: v for k, v in err.items() if v}
            if errs_to_log:
                logger.error(errs_to_log)
                return 1
        else:
            if err:
                logger.error(err)
                return 1
        i += 1
    return 0
