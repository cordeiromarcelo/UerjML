import pandas as pd
import numpy as np

funcs = {
    'Tratamento': ['Preencher Nulos'],
    'Escalonamento': ['Normalize','StandardScaler',
                      'RobustScaler','MinMaxScaler',
                      'OneHotEncoder']
}

options = {
    'Preencher Nulos': ['None', 'False', 'True', '0', '1', '-1', 'Media', 'Moda', 'Mediana'],
}

options_descriptions = {
    'Preencher Nulos': 'Selecione a opção de preenchimento da coluna',
}

