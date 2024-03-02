from ananke.module import BaseContextProcess,BaseModule



# ---------------------------------------------------------------------------- #
#                             ContextProcess Module                            #
# ---------------------------------------------------------------------------- #

# --------------------- Single Module for context process -------------------- #

class ContextCompressor(BaseModule):
    def __init__(self,**kwargs):
        super().__init__()


class ContextTempStorage(BaseModule):
    def __init__(self,**kwargs):
        super().__init__()
        
        
class ContextStructured(BaseModule):
    def __init__(self,**kwargs):
        super().__init__()



# ---------------------------------------------------------------------------- #
#                               Context Processor                              #
# ---------------------------------------------------------------------------- #

# ---------- The final interface of module queue to process context ---------- #

class ContextPrcessor(BaseContextProcess):
    def __init__(self,**kwargs):
        super().__init__()
        
