# -*- coding: utf-8 -*-
def help_default():
    return """
    Usage: codebox COMMAND [ARGS]

    Commands:
      add       Add an item.
      list      List items.
      delete    Delete an item.
      edit      Edit an item.
    """


def help_add():
    return """
    Usage: codebox add [ARGS]
    
    Arguments:
      --help          Show this help message and exit.
      --name TEXT     Specify a name for the snippet. (Required)
      --tags TEXT     Add tags to categorize this snippet. Separate multiple tags with space.
    """


def help_delete():
    return """
    Usage: codebox delete [ARGS] SNIPPET_ID, ...
    
    Arguments:
      --help          Show this help message and exit.
    """


def help_edit():
    return """
    Usage: codebox edit [ARGS] SNIPPET_ID
    
    Arguments:
      --help          Show this help message and exit.
    """


def error_invalid_subcommand():
    return """
    Error: Invalid subcommand.
    """


def error_missing_value(value):
    return f"""
    Error: Missing value after {value}.
    """


def error_missing_argument(value):
    return f"""
    Error: Missing {value} argument.
    """


def error_unknown_argument(value):
    return f"""
    Error: Unknown argument {value}.
    """


def error_saving():
    return f"""
    Error: Snippet not saved.
    """


def error_not_found(value):
    return f"""
    Error: Snippet with ID {value} not found.
    """
