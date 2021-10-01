============================
Litematica Command Generator
============================


.. image:: https://github.com/appcreatorguy/litematica_command_gen/actions/workflows/python-build.yml/badge.svg
        :target: https://github.com/appcreatorguy/litematica_command_gen/actions/workflows/python-build.yml

.. |button| image:: button.png


A CLI application to generate give commands for shulker boxes full of items for litematica projects. Used by the lazy survival player :).


* Free software: GNU General Public License v3


Features
--------

* Convert CSV material lists exported from the Litematica_ mod to give commands for chests full of shulker boxes full of items for said schematic.

Usage
_____

* Download the .whl file from the latest release_ and install it using the following command, where FILENAME is the name of the file you downloaded::
    pip install ./[FILENAME].whl
* Generate a csv material list by holding shift while pressing the 'Write to file' key. |button|
* Run this command::
    litematica-command-gen shulkerbox [PATH]
* PATH will be the path of the .csv file that litematica generated, ususally located in .minecraft/config/litematica.
* Your command will be generated, and can be copied to your clipboard.
* Using a command block, paste the generated command in, and the nearest player will be given a chest full of shulkerboxes with items in them.

Bugs
____

* The parser does not support a large amount of items, more specifically it cannot support more items than what can fill a chest full of shulkerboxes.

Credits
-------

This package was created with Cookiecutter_ and the `appcreatorguy/cookiecutter-pythonpackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`appcreatorguy/cookiecutter-pythonpackage`: https://github.com/appcreatorguy/cookiecutter-pythonpackage
.. _Litematica: https://github.com/maruohon/litematica
.. _release: https://github.com/appcreatorguy/litematica_command_gen/releases/latest
