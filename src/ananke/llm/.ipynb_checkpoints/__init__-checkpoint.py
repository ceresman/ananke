from ananke.base import BaseLocalLLM,BaseRemoteLLM,BaseModule


class LocalModel(BaseLocalLLM):
    def __init__(self,**kwargs):
        super().__init__()
     
        
class RemoteLLM(BaseRemoteLLM):
    def __init__(self,**kwargs):
        super().__init__()
        # self.logger.info(str(self.config()))



