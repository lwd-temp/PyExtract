import logging
import sys
from pathlib import Path

from logger import debug_logger
from utils import config, filename_color

UNWANTED_SUBSTRS = config.rename_substrings


def is_unwanted_substr_present_in_filenames(target_dir) -> bool:
    for path in Path(target_dir).iterdir():
        if path.is_dir():
            continue
        filename = path.name
        if any((substr in filename for substr in UNWANTED_SUBSTRS)):
            return True
    return False


def rename_archives_in_dir(target_dir) -> None:
    for path in Path(target_dir).iterdir():
        if path.is_dir():
            continue
        filename = path.name
        newname, oldname = "", filename
        if any((substr in filename for substr in UNWANTED_SUBSTRS)):
            for substr in UNWANTED_SUBSTRS:
                # print("substr", substr)
                newname = filename.replace(substr, "")
                # print("newname", newname)
            sys.stdout.write(
                "Do you want to rename"
                f" {filename_color(str(path.with_name(oldname)))} to"
                f" {filename_color(str(path.with_name(newname)))} ? [y/n]"
            )
            choice = input().lower()
            if choice in ["y", "Y"]:
                new_path = path.rename(path.with_name(newname))
                debug_logger.info("rename %s to %s", path, new_path)
                print("rename done")
            else:
                print("skip rename")


def main() -> None:
    target_dir = sys.argv[1]
    debug_logger.setLevel(logging.DEBUG)
    rename_archives_in_dir(target_dir=target_dir)


if __name__ == "__main__":
    main()
