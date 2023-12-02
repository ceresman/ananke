# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    code.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 22:46:17 by Winshare To       #+#    #+#              #
#    Updated: 2023/12/02 16:37:06 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



from ananke.base import BaseDocument

        
class CodeDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "CodeDocument"
      

# TODO : Add Executable Support 
# TODO : Add Binary Support       
        
class BinaryDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "BinaryDocument"
        
        
class ExecutableDocument(BaseDocument):
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "ExecutableDocument"
        
   
# class CompressedDocument(BaseDocument):
#     def __init__(self,**kwargs):
#         super().__init__()
#         self.type = "CompressedDocument"
        
        
# class EncryptedDocument(BaseDocument):
#     def __init__(self,**kwargs):
#         super().__init__()
#         self.type = "EncryptedDocument"
        