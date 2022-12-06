import pandas as pd
import numpy as np
import inspect


class Function:
    def __init__(self, function, name, category, options=None, description=None, help_txt=''):
        self.function = function
        self.name = name
        self.category = category
        self.options = options
        self.description = description
        self.help_txt = help_txt

        self.function_params = {}
        for param, info in inspect.signature(self.function).parameters.items():
            self.function_params[param] = {
                "required": 'empty' in str(info.default),
                "type": info.annotation.__name__,
                "default": str(info.default)
            }

    def __call__(self, *args):
        return self.function(*args)


def fill_null(df: pd.DataFrame, columns, value):
    df = df.copy()
    fill_dict = {
        'None': None,
        'False': False,
        'True': True,
        '0': 0,
        '1': 1,
        '-1': -1,
    }

    if not isinstance(columns, list):
        columns = [columns]

    funcs_dict = {
        'Media': 'mean',
        'Moda': 'mode',
        'Mediana': 'median'
    }

    if value in fill_dict.keys():
        df[columns] = df[columns].fillna(fill_dict[value])
        return df

    if value in funcs_dict.keys():
        val_dict = dict(eval(f"df[{columns}].{funcs_dict[value]}()"))
        df[columns] = df[columns].fillna(val_dict)
        return df

    else:
        raise Exception("Esse método não pode ser aplicado")


def remove_nulls(df: pd.DataFrame, columns, value=None):
    df = df.copy()

    if not isinstance(columns, list):
        columns = [columns]

    return df.dropna(subset=columns)


def change_type(df: pd.DataFrame, columns, value):
    df = df.copy()
    types_dict = {
        'Inteiro': 'int',
        'Float': 'float',
        'Long': 'long',
        'Booleano': 'boolean',
        'String(Object)': 'string'
    }

    df[columns] = df[columns].astype(types_dict[value])
    return df


def select_cols(df, columns, value=None):
    df = df.copy()

    if not isinstance(columns, list):
        columns = [columns]

    return df[columns]


def remove_cols(df, columns, value=None):
    df = df.copy()

    if not isinstance(columns, list):
        columns = [columns]

    return df.drop(columns, axis=1)


def round_cols(df, columns, value: int):
    df = df.copy()

    if not isinstance(columns, list):
        columns = [columns]

    df[columns] = df[columns].round(int(value))
    return df


def floor_cols(df, columns, value: int):
    df = df.copy()

    def my_floor(a, precision=0):
        return np.true_divide(np.floor(a * 10 ** precision), 10 ** precision)

    if not isinstance(columns, list):
        columns = [columns]

    df[columns] = df[columns].apply(my_floor, args=[int(value)])
    return df


def ceil_cols(df, columns, value: int):
    df = df.copy()

    def my_ceil(a, precision=0):
        return np.round(a + 0.5 * 10 ** (-precision), precision)

    if not isinstance(columns, list):
        columns = [columns]

    df[columns] = df[columns].apply(my_ceil, args=[int(value)])
    return df
