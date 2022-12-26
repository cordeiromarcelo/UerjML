from abc import ABC, abstractmethod
import pandas as pd
import inspect


class Function(ABC):
    def __init__(self):
        self.args = {}
        for param, info in inspect.signature(self.__call__).parameters.items():
            if param not in ['df', 'columns']:

                if "empty" in str(info.default):
                    default = ""
                else:
                    default = str(info.default)

                self.args[param] = {
                    "required": default == "",
                    "type": info.annotation.__name__,
                    "default": default
                }

    @abstractmethod
    def __call__(self, *args) -> pd.DataFrame:
        return NotImplemented

    @property
    @abstractmethod
    def name(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def category(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def options(self) -> dict[str:list]:
        return NotImplemented

    @property
    @abstractmethod
    def description(self) -> str:
        return NotImplemented

    @property
    @abstractmethod
    def help_txt(self) -> str:
        return NotImplemented
