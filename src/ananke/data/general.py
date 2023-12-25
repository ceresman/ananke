# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    general.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:51:47 by Winshare To       #+#    #+#              #
#    Updated: 2023/12/02 16:37:16 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# ---------------------------------------------------------------------------- #
#                           Current DataType Support                           #
# ---------------------------------------------------------------------------- #
from ananke.base import BaseDocument
from ananke.utils.arxiv_dump import process_pdf

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
        data = process_pdf(filename)
        return data
    
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
        
        
class PostScriptDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "PostScriptDocument"
        
class ElectronicPublicationDocument(BaseDocument):
    """
    EPUB:图文结合，排版自由 & 精美，在各种平台上的阅读体验都不错，也是最受欢迎的格式。
    MOBI、AZW3:阅读效果与 EPUB 差不多，也很不错，多用于 Kindle 电子书阅读器。

    Args:
        BaseDocument (_type_): _description_
    """
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "ElectronicPublicationDocument"
        