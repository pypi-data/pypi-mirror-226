# -*- coding: utf-8 -*-
import os
import sys

from codeboxcli.commands import add
from codeboxcli.commands import delete
from codeboxcli.commands import edit
from codeboxcli.commands import list
from codeboxcli.utils import messages

# Define the path to the directory and the path to the configuration file within that directory
config_dir = os.path.expanduser("~/.codebox")


def cli():
    # Check if the directory doesn't exist, then create it
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Check if there are at least 2 command line arguments (including the script name)
    if len(sys.argv) < 2:
        print(messages.help_default())  # Print the default help message
        return  # Exit the function if no valid subcommand is provided

    subcommand = sys.argv[1]  # Get the subcommand from the second argument
    args = sys.argv[2:]  # Get the remaining arguments as a list

    if subcommand == "add":
        add.add(args)  # Call the 'add' function from the 'commands' module
    elif subcommand == "list":
        list.list()  # Call the 'list' function from the 'commands' module
    elif subcommand == "delete":
        # Call the 'delete' function from the 'commands' module
        delete.delete(args)
    elif subcommand == "edit":
        # Call the 'edit' function from the 'commands' module
        edit.edit(args)
    elif subcommand == "help":
        print(messages.help_default())  # Print the default help message
    else:
        # Print an error message for an invalid subcommand
        print(messages.error_invalid_subcommand())


if __name__ == "__main__":
    cli()  # Call the 'cli' function when the script is executed directly
