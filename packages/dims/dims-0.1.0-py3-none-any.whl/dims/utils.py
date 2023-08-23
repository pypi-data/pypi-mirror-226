import os.path
from pathlib import Path
from typing import Iterable, Optional, Union


def read_all_recursively(base: Union[Path, str], pattern: Optional[str] = "*") -> list[str]:
    """
    Recursively reads all files in the provided path
    """
    if not isinstance(base, Path):
        base = Path(base)

    base = base.expanduser()

    if not os.path.exists(base):
        msg = f"invalid path provided: {base}"
        raise ValueError(msg)

    if not os.path.isdir(base):
        msg = f"provided path is not a directory: {base}"
        raise ValueError(msg)

    return [str(path.relative_to(base)) for path in base.rglob(pattern)]


def get_unique_filenames(paths: Iterable[str], base: Path) -> set[str]:
    """
    For the provided path, find all unique file names
    """
    filenames: set[str] = set()

    for path in paths:
        full_path = base / path
        if os.path.isfile(full_path):
            filenames.add(full_path.name)

    return filenames


def compare_paths(src: Union[Path, str], target: Union[Path, str], *, exact_paths: bool = True) -> list[str]:
    """
    By default, this returns any missing paths from the src path that are not in the target
    path.

    When the exact_paths arguments is set to False it will use the *unique* file names to
    find any missing values.
    """
    src_base = Path(src)
    target_base = Path(target)
    src_paths = read_all_recursively(src_base)
    target_paths = read_all_recursively(target_base)

    if exact_paths:
        src_set = set(src_paths)
        target_set = set(target_paths)

        return [str(path) for path in src_set - target_set]

    src_file_set = get_unique_filenames(src_paths, src_base)
    target_file_set = get_unique_filenames(target_paths, target_base)

    return list(src_file_set - target_file_set)
