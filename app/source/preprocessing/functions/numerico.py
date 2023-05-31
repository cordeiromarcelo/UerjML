import pandas as pd
import numpy as np
from app.source.preprocessing.function_class import Function


class RoundCols(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str], casas: int) -> pd.DataFrame:
        """
        Arredonde uma matriz para o número determinado de decimais

        Parâmeteros
        ----------
        casas: int
            Quantidade de casas decimais
        """

        df = df.copy()

        if not isinstance(columns, list):
            columns = [columns]

        df[columns] = df[columns].round(int(casas))
        return df

    @property
    def name(self) -> str:
        return 'Arredondar'

    @property
    def category(self) -> str:
        return 'Numérico'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return 'Selecione a quantidade de casas decimais'

    @property
    def help_txt(self) -> str:
        return """Arredonde uma matriz para o número determinado de decimais"""


class FloorCols(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str], casas: int) -> pd.DataFrame:
        """
        Arredonda para baixo, elemento a elemento.
        Matematicamente, o valor arredondado x é o maior inteiro i, tal que i <= x.

        Parâmeteros
        ----------
        casas: int
            Quantidade de casas decimais
        """

        df = df.copy()

        def my_floor(a, precision=0):
            return np.true_divide(np.floor(a * 10 ** precision), 10 ** precision)

        if not isinstance(columns, list):
            columns = [columns]

        df[columns] = df[columns].apply(my_floor, args=[int(casas)])
        return df

    @property
    def name(self) -> str:
        return 'Arredondar para Baixo'

    @property
    def category(self) -> str:
        return 'Numérico'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return 'Selecione a quantidade de casas decimais'

    @property
    def help_txt(self) -> str:
        return """Arredonda para baixo, elemento a elemento.
               Matematicamente, o valor arredondado x é o maior inteiro i, tal que i <= x."""


class CeilCols(Function):
    def __call__(self, df: pd.DataFrame, columns: list[str], casas: int) -> pd.DataFrame:
        """
        Arredonda para cima, elemento a elemento.
        Matematicamente, o valor arredondado x é o menor inteiro i, tal que i >= x.

        Parâmeteros
        ----------
        casas: int
            Quantidade de casas decimais
        """

        df = df.copy()

        def my_ceil(a, precision=0):
            return np.round(a + 0.5 * 10 ** (-precision), precision)

        if not isinstance(columns, list):
            columns = [columns]

        df[columns] = df[columns].apply(my_ceil, args=[int(casas)])
        return df

    @property
    def name(self) -> str:
        return 'Arredondar para Cima'

    @property
    def category(self) -> str:
        return 'Numérico'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return 'Selecione a quantidade de casas decimais'

    @property
    def help_txt(self) -> str:
        return """Arredonda para cima, elemento a elemento.
               Matematicamente, o valor arredondado x é o menor inteiro i, tal que i >= x."""