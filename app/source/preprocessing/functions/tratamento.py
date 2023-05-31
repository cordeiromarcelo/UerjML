import pandas as pd
import numpy as np
from app.source.preprocessing.function_class import Function


class FillNull(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str], preencher: str) -> pd.DataFrame:
        """
        Preenche os valores nulos das colunas
        selecionadas com o método ou valor selecionado

        Parâmeteros
        ----------
        preencher: str
            Valor de preenchimento dos nulos
        """
        df = df.copy()

        if not isinstance(columns, list):
            columns = [columns]

        funcs_dict = {
            'Media': 'mean',
            'Moda': 'mode',
            'Mediana': 'median'
        }

        if preencher in funcs_dict.keys():
            val_dict = dict(eval(f"df[{columns}].{funcs_dict[preencher]}()"))
            df[columns] = df[columns].fillna(val_dict)
            return df
        else:
            df[columns] = df[columns].fillna(preencher)
            return df

    @property
    def name(self) -> str:
        return 'Preencher Nulos'

    @property
    def category(self) -> str:
        return 'Tratamento'

    @property
    def options(self) -> dict[str:list]:
        return {'preencher': ['None', 'False', 'True', '0', '1', '-1', 'Media', 'Moda', 'Mediana']}

    @property
    def description(self) -> str:
        return 'Selecione a opção de preenchimento da coluna'

    @property
    def help_txt(self) -> str:
        return 'Preenche os valores nulos das colunas selecionadas com o método ou valor selecionado'


class RemoveNulls(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Remove da base de dados todas as linhas que contenham
        valores nulos em qualquer uma das colunas selecionadas
        """

        df = df.copy()

        if not isinstance(columns, list):
            columns = [columns]

        return df.dropna(subset=columns)

    @property
    def name(self) -> str:
        return 'Remover Nulos'

    @property
    def category(self) -> str:
        return 'Tratamento'

    @property
    def options(self):
        return None

    @property
    def description(self):
        return None

    @property
    def help_txt(self) -> str:
        return """Remove da base de dados todas as linhas que contenham
               valores nulos em qualquer uma das colunas selecionadas"""


class ChangeType(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str], tipo: str, test: str) -> pd.DataFrame:
        """
        Converte o tipo de dado das colunas selecionadas para o
        tipo de dado selecionado

        Parâmeteros
        ----------
        tipo: str
            Para qual tipo será a alteração
        """

        df = df.copy()
        types_dict = {
            'Inteiro': 'int',
            'Float': 'float',
            'Long': 'long',
            'Booleano': 'boolean',
            'String(Object)': 'string'
        }

        df[columns] = df[columns].astype(types_dict[tipo])
        return df

    @property
    def name(self) -> str:
        return 'Alterar Tipo'

    @property
    def category(self) -> str:
        return 'Tratamento'

    @property
    def options(self) -> dict[str:list]:
        return {'tipo': ['Inteiro', 'Float', 'Long', 'Booleano', 'String(Object)']}

    @property
    def description(self):
        return 'Selecione para qual tipo de dado deseja alterar'

    @property
    def help_txt(self) -> str:
        return """Converte o tipo de dado das colunas selecionadas para o
        tipo de dado selecionado"""