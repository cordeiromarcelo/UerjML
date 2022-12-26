import pandas as pd
import numpy as np
from preprocessing.function_class import Function


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
        return 'Selecão'

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
        return 'Selecão'

    @property
    def options(self) -> dict[str:list]:
        return None

    @property
    def description(self):
        return None

    @property
    def help_txt(self) -> str:
        return 'Remove as colunas selecionadas da base de dados'
