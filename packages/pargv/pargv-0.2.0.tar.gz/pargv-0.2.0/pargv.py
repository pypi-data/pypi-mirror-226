import sys


__version__ = '0.2.0'


def parse_args(argv=None):
    """
    Returns a tuple of (args, kwargs) from a given list of command line arguments.
    Defaults to using `sys.argv`.
    """
    argv = argv if argv else sys.argv

    args = []
    for arg in argv:
        if arg.startswith('-'):
            break
        args.append(arg.replace('-', '_'))

    kwargs = {}
    value = None
    for arg in argv[len(args):]:

        if not arg.startswith('-'):
            if isinstance(kwargs[key], bool):
                kwargs[key] = arg
            elif isinstance(kwargs[key], str):
                kwargs[key] = [kwargs[key]] + [arg]
            elif isinstance(kwargs[key], list):
                kwargs[key].append(arg)
            continue

        key = arg[:2].lstrip('-') + arg[2:].replace('-', '_')

        if '=' in key:
            key, value = key.split('=')

        if not arg.startswith('--'):
            for k in key[:-1]:
                kwargs[k] = True
            key = key[-1]

        kwargs[key] = value if value else True
        value = None

    return (args, kwargs)
