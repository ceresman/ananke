from typing import Any
from base import BaseModule
from abc import ABC,abstractmethod


class Module(BaseModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.__class__.__name__
        self.logger.info(self.__class__.__name)

    @abstractmethod
    def forward(self, data: Any, **kwargs):
        raise NotImplementedError("Implement the forward method in the module class.")
    
    
    def __call__(self, data : Any, **kwargs: Any) -> Any:
        return self.forward(data, **kwargs)
    
    