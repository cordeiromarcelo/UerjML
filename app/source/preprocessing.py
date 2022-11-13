import pandas as pd
import numpy as np
import functions as f

functions_list = [
    f.Function(function=f.fill_null,
               name='Preencher Nulos',
               category='Tratamento',
               options=['None', 'False', 'True', '0', '1', '-1', 'Media', 'Moda', 'Mediana'],
               description='Selecione a opção de preenchimento da coluna'),

    f.Function(function=f.remove_nulls,
               name='Remover Nulos',
               category='Tratamento'),

    f.Function(function=f.change_type,
               name='Alterar Tipo',
               category='Tratamento',
               options=['Inteiro', 'Float', 'Long', 'Booleano', 'String(Object)'],
               description='Selecione para qual tipo de dado deseja alterar'),

    f.Function(function=f.select_cols,
               name='Selecionar Colunas',
               category='Selecão'),

    f.Function(function=f.remove_cols,
               name='Remover Colunas',
               category='Selecão'),

    f.Function(function=f.round_cols,
               name='Arredondar',
               category='Numérico',
               options=[str(i) for i in range(10)],
               description='Selecione a quantidade de casas decimais'),

    f.Function(function=f.floor_cols,
               name='Arredondar para Baixo',
               category='Numérico',
               options=[str(i) for i in range(10)],
               description='Selecione a quantidade de casas decimais'),

    f.Function(function=f.ceil_cols,
               name='Arredondar para Cima',
               category='Numérico',
               options=[str(i) for i in range(10)],
               description='Selecione a quantidade de casas decimais'),
]

name_funcs_dict = dict(zip([function.name for function in functions_list], functions_list))

category_funcs_dict = {}
for category in np.unique([function.category for function in functions_list]):
    category_funcs_dict[category] = [function.name for function in functions_list if function.category == category]

funcs_options_dict = {function.name: function.options for function in functions_list if function.options is not None}

options_descriptions_dict = {function.name:function.description for function in functions_list if function.description is not None}
