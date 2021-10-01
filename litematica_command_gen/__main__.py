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
import cli
import command_generator as generator
from docopt import docopt

from . import __version__

if __name__ == "__main__":
    cli.main()
