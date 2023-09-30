from ananke.base import BaseLocalLLM,BaseRemoteLLM,BaseModule


class LocalEmbedding(BaseModule):
    def __init__(self,**kwargs):
        super().__init__()


class LocalLLM(BaseLocalLLM):
    def __init__(self,**kwargs):
        super().__init__()
        

class RemoteEmbedding(BaseModule):
    def __init__(self,**kwargs):
        super().__init__()
        
        
class RemoteLLM(BaseRemoteLLM):
    def __init__(self,**kwargs):
        super().__init__()


