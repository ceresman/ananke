# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    general.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:51:47 by Winshare To       #+#    #+#              #
#    Updated: 2023/09/30 09:54:00 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# ---------------------------------------------------------------------------- #
#                           Current DataType Support                           #
# ---------------------------------------------------------------------------- #
from ananke.base import BaseDocument


class Paper(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "Paper"
        
    def read(self,filename):
        """academy article reader

        Args:
            filename (_type_): _description_
        """
        self.logger.debug(str(self.__class__.__name__)+" module read : "+str(filename))
        pass
    
    def write(self,outputname):
        self.logger.debug(str(self.__class__.__name__)+" module write : "+str(outputname))
        pass
        
class WordDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "WordDocument"
        
        
class PowerPointDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "PowerPointDocument"
        
        
        
        
class PDFDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "PDFDocument"
        
        
class TextDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "TextDocument"
        


class MarkdownDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "MarkdownDocument"
               
        
class WebPageDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "WebPageDocument"
        
        
class LaTeXDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "LaTeXDocument"
        