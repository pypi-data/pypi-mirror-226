#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse


# nagios return codes
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2


def get_args():
    parser = argparse.ArgumentParser(
        description=(
            "Checks whether PHP files have valid syntax, primarily used for checking"
            " automatically generated files"
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        required=True,
        help="path which will be scanned for PHP files, including subdirectories",
    )
    return parser.parse_args()


def main():
    dir = get_args().directory
    os.chdir(dir)
    paths = []
    for (
        dirpath,
        dirname,
        filenames,
    ) in os.walk("."):
        for f in filenames:
            if f.endswith(".php"):
                paths.append(
                    os.path.join(
                        dirpath,
                        f,
                    )
                )
    global_result = ""

    for path in paths:
        if os.path.isfile(path):
            result = subprocess.getoutput(f"php -l {path}")
            if not result.startswith("No syntax errors"):
                global_result += f"{result}  |  "

    if not global_result:
        print(f"{OK} check_php_syntax - OK")
        sys.exit(OK)
    else:
        print(f"{CRITICAL} check_php_syntax - {global_result}")
        sys.exit(CRITICAL)


if __name__ == "__main__":
    main()
