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

from . import __version__
from .litematica_command_gen import main

if __name__ == "__main__":
    args = docopt(__doc__, version=__version__)
    if args["--verbose"]:
        print("Running with arguments: ", end="")
        print("".join(["{0}: {1}, ".format(k, v) for k, v in args.items()]))
    command = main(args["shulkerbox"], args["chest"], args["<file>"], args["--verbose"])
