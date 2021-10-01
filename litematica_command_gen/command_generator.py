"""Main Module."""
import csv
from pathlib import Path

import pandas as pd
from mecha import Mecha

from . import mc_id_converter as mc

mecha_obj = Mecha()

usingshulkerbox = False  # ? True if chest is passed instead of shulkerbox
verbosity = False  # ? True if verbose
line_count = 0  # ? Number of lines in the file.

STACK_SIZE = 64  # ? Number of item in a stack.
COMMAND_START = """
execute
    as @p
    run
        give
            @s
            chest{
                BlockEntityTag:{
                    Items:[
                        {
                            Slot:0b,id:"minecraft:shulker_box",Count:1b,tag:{
                                BlockEntityTag:{
                                    Items:[
"""
COMMAND_NEW_SHULKER_BOX_START = """
                                    ]
                                }
                            }
                        },
                        {
                            Slot:"""
COMMAND_NEW_SHULKER_BOX_END = """b,id:"minecraft:shulker_box",Count:1b,tag:{
                                BlockEntityTag:{
                                    Items:[
"""
COMMAND_END = """
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
            1
"""


def generate_command_from_file(shulkerbox, chest, file, verbose):
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

    print("Usingshulkerbox: {}".format(usingshulkerbox)) if verbose else None

    data_dict = read_csv_file(file)
    print("File read.") if verbose else None

    formatted_items = format_all_items(data_dict)

    command = generate_command(formatted_items) if usingshulkerbox else None

    ast = mecha_obj.parse(command, multiline=True)
    final_command = mecha_obj.serialize(ast)
    return final_command


def read_csv_file(file):
    """Read a csv file and return a nested dictionary of its contents

    Args:
        file (str): the path of the files

    Raises:
        FileNotFoundError: The file does not exist, or was not found

    Returns:
        dict: a nested dict of the file's values
    """
    path = Path(file)
    try:
        data_dict = dict()
        # global data
        # data = path.read_text().replace('"', "")
        with open(path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for count, row in enumerate(reader):
                data_dict.__setitem__(count, row)
        return data_dict
    except FileNotFoundError:
        raise FileNotFoundError(
            "The specified file: '{0}' does not exist".format(path.name)
        )


def generate_command(data):
    # TODO: Support multiple chests
    command = [COMMAND_START]  # Array of strings to concat to form final command
    item_index = 0
    box_count = 0
    for row in data.itertuples():
        if box_count >= 27:
            break
        if (
            row.Index == 0 or row.Index % 27 != 0
        ):  # Number of slots in single shulkerbox
            item_index = row.Index - (27 * box_count)  # Resets item Count for new box
            if row.Index == 0:
                command_segment = (
                    "{"
                    + 'Slot:{0}b,id:"{1}",Count:{2}b'.format(
                        item_index, row.item, row.count
                    )
                    + "}"
                )
            else:
                command_segment = (
                    ",\n{"
                    + 'Slot:{0}b,id:"{1}",Count:{2}b'.format(
                        item_index, row.item, row.count
                    )
                    + "}"
                )
            command.append(command_segment)
        else:
            box_count += 1
            item_index = row.Index - (27 * box_count)  # Resets item Count for new box
            command.append(
                COMMAND_NEW_SHULKER_BOX_START
                + str(box_count)
                + COMMAND_NEW_SHULKER_BOX_END
            )
            command_segment = (
                "{"
                + 'Slot:{0}b,id:"{1}",Count:{2}b'.format(
                    item_index, row.item, row.count
                )
                + "}"
            )
            command.append(command_segment)

    command.append(COMMAND_END)
    return "".join(command)


def format_all_items(data):
    """Generate a DataFrame from a nested dictionary of item names and counts.

    Args:
        data (Dict): A nested dictionary of dictionaries in the format {item name:total:...}

    Raises:
        TypeError: If the file is incorrectly formatted and there are no nested dictionaries

    Returns:
        DataFrame: A Pandas DataFrame in the format 'item count'
    """
    formatted_items = pd.DataFrame(
        columns=["item", "count"]
    )  # ? Stored in format 'item_id:count'
    for (
        item
    ) in (
        data.values()
    ):  # Item should be another dict containing data for a single item type
        if type(item) == dict:
            item_df = generate_item_dict(item)
            frames = [formatted_items, item_df]
            formatted_items = pd.concat(frames, ignore_index=True)
        else:
            raise TypeError("Incorrectly formatted file.")
    return formatted_items


def generate_item_dict(item):
    """Generate a DataFrame for a single item type.

    Args:
        item (Dict): A Dictionary in the format{'Item', 'Total', ...}

    Raises:
        KeyError: If the dictionary is in an incorrect format

    Returns:
        DataFrame: A dataframe in the format 'item count' seperated into stacks
    """
    return_dict = pd.DataFrame(columns=["item", "count"])
    number_of_stacks = 0
    remainder_stack_count = 0
    try:
        block_name = item["Item"]
        block_id = mc.block_name_to_id(block_name)

        count = int(item["Total"])
        number_of_stacks = count // STACK_SIZE
        remainder_stack_count = count % STACK_SIZE
        for i in range(number_of_stacks):
            return_dict.loc[len(return_dict)] = [block_id, 64]
        if remainder_stack_count != 0:
            return_dict.loc[len(return_dict)] = [block_id, remainder_stack_count]
    except KeyError:
        raise KeyError(
            "Incorrectly formatted file. Keys 'Item' or 'Total' were not present."
        )
    return return_dict
