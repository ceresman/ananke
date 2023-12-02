from ananke.module import BaseContextProcess,Module



# ---------------------------------------------------------------------------- #
#                             ContextProcess Module                            #
# ---------------------------------------------------------------------------- #

# --------------------- Single Module for context process -------------------- #

class ContextCompressor(Module):
    def __init__(self,**kwargs):
        super().__init__()


class ContextTempStorage(Module):
    def __init__(self,**kwargs):
        super().__init__()
        
        
class ContextStructured(Module):
    def __init__(self,**kwargs):
        super().__init__()



# ---------------------------------------------------------------------------- #
#                               Context Processor                              #
# ---------------------------------------------------------------------------- #

# ---------- The final interface of module queue to process context ---------- #

class ContextPrcessor(Module):
    def __init__(self,**kwargs):
        super().__init__()
        
