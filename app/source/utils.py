from ast import literal_eval


def simplest_type(s):
    try:
        return literal_eval(s)
    except:
        return s


def fix_args_types(args_list):
    return [simplest_type(arg) for arg in args_list]
