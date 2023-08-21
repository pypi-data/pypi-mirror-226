def get_prefix(name):
    """Get the prefix of a name.

    Args:
        name (str): A name.

    Returns:
        str: The prefix of the name.
    """
    if len(name) == 1:
        return "-"
    else:
        return "--"


def parse_list_arg(name, arg):
    """Parse a list argument.

    Args:
        arg (list[str]): A list argument.

    Returns:
        A string representing the argument, prepended with the argument name.
    """
    return " ".join([f"{get_prefix(name)}{name} {env}" for env in arg])


def parse_scalar_arg(name, arg):
    """Parse a scalar argument.

    Args:
        arg (str): A scalar argument.

    Returns:
        A string representing the argument, prepended with the argument name.
    """

    if isinstance(arg, bool):
        arg_string = arg
    elif isinstance(arg, str):
        arg_string = f'"{arg}"'
    else:
        arg_string = arg

    return f"{get_prefix(name)}{name} {arg_string}"


def generate_args(args):
    """Generate a list of arguments from a parsed YAML file.

    Args:
        parsed_yaml (dict): A parsed YAML file.

    Returns:
        list: A list of arguments.
    """
    arg_strings = []
    for name, arg in args.items():
        clean_name = name.replace("_", "-")
        if name.startswith("_pos") and isinstance(arg, str):
            arg_strings.append(arg)
        elif name.startswith("_pos") and isinstance(arg, list):
            arg_strings.extend(arg)
        elif name.startswith("_"):
            continue
        elif isinstance(arg, list):
            arg_strings.append(parse_list_arg(clean_name, arg))
        else:
            arg_strings.append(parse_scalar_arg(clean_name, arg))

    return arg_strings
