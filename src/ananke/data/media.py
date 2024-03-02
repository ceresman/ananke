
from ananke.base import BaseMedia

class ImageDocument(BaseMedia):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "ImageDocument"
        
                
class VideoDocument(BaseMedia):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "VideoDocument"
        
                
class AudioDocument(BaseMedia):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "AudioDocument"
        