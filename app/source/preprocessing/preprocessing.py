import numpy as np
import inspect

from preprocessing import functions

clsmembers = inspect.getmembers(functions, inspect.isclass)
functions_list = [obj() for name, obj in clsmembers if name != 'Function']

name_funcs_dict = dict(zip([function.name for function in functions_list], functions_list))

category_funcs_dict = {}
for category in np.unique([function.category for function in functions_list]):
    category_funcs_dict[category] = [function.name for function in functions_list if function.category == category]

funcs_options_dict = {function.name: function.options for function in functions_list}

options_descriptions_dict = {function.name: function.description for function in functions_list}

funcs_helps_dict = {function.name: function.help_txt for function in functions_list}

func_args_dict = {function.name: function.args for function in functions_list}