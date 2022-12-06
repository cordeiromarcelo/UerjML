import pandas as pd
import numpy as np
import functions as f

functions_list = [
    f.Function(function=f.fill_null,
               name='Preencher Nulos',
               category='Tratamento',
               options=['None', 'False', 'True', '0', '1', '-1', 'Media', 'Moda', 'Mediana'],
               description='Selecione a opção de preenchimento da coluna',
               help_txt='Preenche os valores nulos das colunas selecionadas com o método ou valor selecionado'),

    f.Function(function=f.remove_nulls,
               name='Remover Nulos',
               category='Tratamento',
               help_txt='''Remove da base de dados todas as linhas que contenham
               valores nulos em qualquer uma das colunas selecionadas'''),

    f.Function(function=f.change_type,
               name='Alterar Tipo',
               category='Tratamento',
               options=['Inteiro', 'Float', 'Long', 'Booleano', 'String(Object)'],
               description='Selecione para qual tipo de dado deseja alterar',
               help_txt='Converte o tipo de dado das colunas selecionadas para o tipo de dado selecionado'),

    f.Function(function=f.select_cols,
               name='Selecionar Colunas',
               category='Selecão',
               help_txt='Mantém somente as colunas selecionadas na base de dados'),

    f.Function(function=f.remove_cols,
               name='Remover Colunas',
               category='Selecão',
               help_txt='Remove as colunas selecionadas da base de dados'),

    f.Function(function=f.round_cols,
               name='Arredondar',
               category='Numérico',
               options=[],
               description='Selecione a quantidade de casas decimais',
               help_txt="Arredonde uma matriz para o número determinado de decimais."),

    f.Function(function=f.floor_cols,
               name='Arredondar para Baixo',
               category='Numérico',
               options=[str(i) for i in range(10)],
               description='Selecione a quantidade de casas decimais',
               help_txt='''Arredonda para baixo, elemento a elemento.
               Matematicamente, o valor arredondado x é o maior inteiro i, tal que i <= x.'''),

    f.Function(function=f.ceil_cols,
               name='Arredondar para Cima',
               category='Numérico',
               options=[str(i) for i in range(10)],
               description='Selecione a quantidade de casas decimais',
               help_txt='''Arredonda para cima, elemento a elemento.
               Matematicamente, o valor arredondado x é o menor inteiro i, tal que i >= x''')
    ]

name_funcs_dict = dict(zip([function.name for function in functions_list], functions_list))

category_funcs_dict = {}
for category in np.unique([function.category for function in functions_list]):
    category_funcs_dict[category] = [function.name for function in functions_list if function.category == category]

funcs_options_dict = {function.name: function.options for function in functions_list if function.options is not None}

options_descriptions_dict = {function.name: function.description for function in functions_list if function.description is not None}

funcs_helps_dict = {function.name: function.help_txt for function in functions_list}