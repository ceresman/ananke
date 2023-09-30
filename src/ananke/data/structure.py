
from ananke.base import BaseDocument
        
class CSVDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "CSVDocument"
        
class ExcelDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "ExcelDocument"