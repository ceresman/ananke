from ananke.base import BaseServer,BaseClient

class Server(BaseServer):
    def __init__(self,**kwargs):
        super().__init__()
        
class Client(BaseClient):
    def __init__(self,**kwargs):
        super().__init__()