"""Litematica Give Command Generator.

Usage:
    cli.py (shulkerbox|chest) <file> [--verbose]
    cli.py (-h | --help)
    cli.py --version

Options:
    -h, --help     Show this screen.
    --version      Show version.
    --verbose      Print more text.

"""
from docopt import docopt

from . import __version__ as VERSION
from .command_generator import generate_command_from_file


def main():
    args = docopt(__doc__, version=VERSION)
    if args["--verbose"]:
        print("Running with arguments: ", end="")
        print("".join(["{0}: {1}, ".format(k, v) for k, v in args.items()]))
    command = generate_command_from_file(
        True, args["chest"], args["<file>"], args["--verbose"]
    )
    print(command)
    print("\n\n\n")
    s = ""
    while s not in ["Y", "N"]:
        s = input("Copy to clipboard? (Y/N):").upper()
    if s == "Y":
        from pandas.io import clipboards

        clipboards.to_clipboard(obj=command, excel=False)


if __name__ == "__main__":
    main()
