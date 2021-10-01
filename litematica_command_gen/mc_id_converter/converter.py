"""Convert item and block names to ids and vice versa."""
import os
from pathlib import Path, WindowsPath

import pandas as pd

# url = "https://minecraft.fandom.com/wiki/Java_Edition_data_values?variant=en"
thisfile = os.path.dirname(os.path.abspath(__file__))
url = Path(thisfile).joinpath(Path("data/block_data.html")).read_text()
table = None
MINECRAFT_NAMESPACE = "minecraft"


def block_name_to_id(block_name):
    """Convert a block name to its namespaced id.

    Args:
        block_name (str): the name of the block to convert

    Returns:
        str: the namespaced id of the block
    """
    global table
    if table is None:
        generate_table()

    block_name = " ".join(block_name.split())

    # SPECIAL CASES FOR BLOCKS THAT DON'T HAVE ITEMS
    if block_name == "Redstone Dust":
        return ":".join([MINECRAFT_NAMESPACE, "redstone"])
    elif block_name == "Water Bucket":
        return ":".join([MINECRAFT_NAMESPACE, "water_bucket"])
    elif block_name == "Lava Bucket":
        return ":".join([MINECRAFT_NAMESPACE, "lava_bucket"])
    elif block_name == "Redstone Block":
        return ":".join([MINECRAFT_NAMESPACE, "redstone_block"])

    for i in range(len(table.Block)):
        if " ".join(table.Block[i].split()) == block_name:
            return ":".join([MINECRAFT_NAMESPACE, table.ResourceLocation[i]])


def generate_table():
    global table
    table = pd.read_html(
        url, header=0, converters={"Block": str, "Resource Location": str}
    )[0]
