import pandas as pd
import numpy as np
from app.source.preprocessing.function_class import Function


class SelectCols(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Mantém somente as colunas selecionadas na base de dados
        """
        df = df.copy()

        if not isinstance(columns, list):
            columns = [columns]

        return df[columns]

    @property
    def name(self) -> str:
        return 'Selecionar Colunas'

    @property
    def category(self) -> str:
        return 'Colunas'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return None

    @property
    def help_txt(self) -> str:
        return 'Mantém somente as colunas selecionadas na base de dados'


class RemoveCols(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Remove as colunas selecionadas da base de dados
        """
        df = df.copy()

        if not isinstance(columns, list):
            columns = [columns]

        return df.drop(columns, axis=1)

    @property
    def name(self) -> str:
        return 'Remover Colunas'

    @property
    def category(self) -> str:
        return 'Colunas'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return None

    @property
    def help_txt(self) -> str:
        return 'Remove as colunas selecionadas da base de dados'


class CreateColumns(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str] = None, text: str = '') -> pd.DataFrame:
        """
        Avalie uma string descrevendo operações em colunas DataFrame.
        Opera apenas em colunas, não em linhas ou elementos específicos.

        Exemplos:
            df.eval('C = A + B')
            df.eval('A + B')
            df.eval(
                '''
                C = A + B
                D = A - B
                '''
            )

        Parâmeteros
        ----------
        casas: int
            Quantidade de casas decimais
        """

        df = df.copy()

        df.eval(text, inplace=True)
        return df

    @property
    def name(self) -> str:
        return 'Criar Coluna'

    @property
    def category(self) -> str:
        return 'Colunas'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return 'Descreva a operação a ser realizada. Ex: Col_C = Col_A + Col_B'

    @property
    def help_txt(self) -> str:
        return """Avalie uma string descrevendo operações em colunas do DataFrame.
        Opera apenas em colunas, não em linhas ou elementos específicos.

        Exemplos:
            Col_C = Col_A + Col_B
            Col_D = (Col_A + Col_B) / Col_C
        """


class QueryFilter(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str] = None, text: str = '') -> pd.DataFrame:
        """
        Filtre as colunas de um DataFrame com uma expressão booleana.

        Você pode se referir a nomes de colunas que não são nomes de variáveis Python válidos colocando-os entre crases.
        Por exemplo, uma coluna chamada “Area (cm^2)” seria referenciada como `Area (cm^2)`

        Exemplos:
            df.query('B == `C C`')

        Parâmeteros
        ----------
        casas: int
            Quantidade de casas decimais
        """

        df = df.copy()

        df.query(text, inplace=True)
        return df

    @property
    def name(self) -> str:
        return 'Filtrar Colunas'

    @property
    def category(self) -> str:
        return 'Colunas'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return """Filtre as colunas de um DataFrame com uma expressão booleana.
        Ex: (Col_A > 5) & (Col_B == `Col_C (cm^2)`)"""

    @property
    def help_txt(self) -> str:
        return """Filtre as colunas de um DataFrame com uma expressão booleana.

        Você pode se referir a nomes de colunas que não são nomes de variáveis Python válidos colocando-os entre crases.
        Por exemplo, uma coluna chamada “Area (cm^2)” seria referenciada como `Area (cm^2)`

        Exemplos:
            Col_A > 5
            Col_B == `Col_C (cm^2)`

        """