from typing import Any
from ananke.base import BaseModule
from abc import ABC,abstractmethod
import threading

class Module(BaseModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "name" not in kwargs.keys():
            self.name = self.__class__.__name__
        else:
            self.name = kwargs["name"]
        self.logger.info("base module init"+self.name)

    @abstractmethod
    def forward(self, data: Any, **kwargs):
        raise NotImplementedError("Implement the forward method in the module class.")
    
    
    def threading_info(self):
        self.logger.debug("threading:"+str(threading.current_thread().name))
    
    def __call__(self, data : Any, **kwargs: Any) -> Any:
        return self.forward(data, **kwargs)




class Retriever(BaseModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.__class__.__name__
        self.logger.info(self.name)

    @abstractmethod
    def forward(self, data: Any, **kwargs):
        raise NotImplementedError("Implement the forward method in the module class.")


    def __call__(self, data : Any, **kwargs: Any) -> Any:
        return self.forward(data, **kwargs)
    
    
class APIS(Module):
    def __init__(self):
        # Initialize any necessary data framework state here
        # 该类链接指定的数据架构，里面只包含全部的内部系统级API
        super().__init__()

class TempStorage(Module):
    def __init__(self):
        # Initialize any necessary data framework state here
        # 该类链接指定的数据架构指向的临时持久化存储，里面只包含当前Session的全部内容
        super().__init__()
        
class Template(Module):
    def __init__(self):
        # Initialize any necessary data framework state here
        # 该类链接指定的数据架构指向的模板，里面只包含当前生成任务模板
        super().__init__()
        
class DataFrameworkClient(Module):
    def __init__(self):
        # Initialize any necessary data framework state here
        # 该类链接指定的数据架构，里面只包含指定的数据框架交互客户端
        super().__init__()