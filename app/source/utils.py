from ast import literal_eval


def simplest_type(s):
    try:
        return literal_eval(s)
    except:
        return s


def fix_kwargs_types(kwarg_list):
    return [simplest_type(kwarg) for kwarg in kwarg_list]
