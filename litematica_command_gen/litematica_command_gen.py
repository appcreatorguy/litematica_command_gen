"""Main Module."""
import csv
from pathlib import Path

import mc_id_converter as mc

command = (
    []
)  # ? List of strings that will be concatenated together to form the final command.
usingshulkerbox = False  # ? True if chest is passed instead of shulkerbox
verbosity = False  # ? True if verbose
data = None  # ? Array of csv data imported from the given file path.
line_count = 0  # ? Number of lines in the file.


def main(shulkerbox, chest, file, verbose):
    """Main Entry point for generator

    Args:
        shulkerbox (bool): True if generating a shulkerbox
        chest (bool): True if generating a chest
        file (str): csv data file location
        verbose (bool): Verbosity

    Raises:
        ValueError: If neither chest nor shulkerbox are passed.

    Returns:
        str: Generated command string.
    """
    global usingshulkerbox
    if shulkerbox and not chest:
        usingshulkerbox = True
    elif chest and not shulkerbox:
        usingshulkerbox = False
    else:
        raise ValueError(
            "neither 'shulkerbox' nor 'chest' were passed to the program."
        )  # Should never actually happen from commandline, only here if called from another module
    if verbose:
        global verbosity
        verbosity = True

    print("Usingshulkerbox: {}".format(usingshulkerbox))

    read_file(file)
    print("File read.") if verbose else None
    global data
    generate_command(data)

    global command
    print("".join(command))
    return "".join(command)


def read_file(file):
    """Read and store file data safely

    Args:
        file (str): File location

    Raises:
        FileNotFoundError: Raised if file doesn't exist
    """
    path = Path(file)
    try:
        global data
        data = path.read_text().replace('"', "")
    except FileNotFoundError:
        raise FileNotFoundError(
            "The specified file: '{0}' does not exist".format(path.name)
        )

    global line_count
    with path.open(mode="r") as f:
        line_count = sum(1 for line in f)


def generate_command(data):
    global command
    csv_reader = csv.reader(data.splitlines(), delimiter=",")
    row_count = 0
    for row in csv_reader:
        if row_count == 0:
            command.append('/give @s shulker_box{BlockEntityTag:{Items:[{Slot:0b,id:"')
        else:
            block = mc.block_name_to_id(row[0])
            if int(row[2]) <= 64 and row_count != line_count - 1:
                appending = block + (
                    '",Count:{0}b'.format(row[2])
                    + "},{"
                    + 'Slot:{0}b,id:"'.format(row_count)
                )
                command.append(appending)
                print(appending) if verbosity else None
        if row_count == 27:
            appending = '",Count:1b}]}} 1'
            command.append(appending)
            break
        row_count += 1
