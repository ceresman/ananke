# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    hugginface.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/29 21:45:15 by Winshare To       #+#    #+#              #
#    Updated: 2023/10/01 18:38:40 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ananke.llm import RemoteLLM,RemoteEmbedding,LocalEmbedding,LocalLLM
from abc import ABC,abstractmethod

class HuggingfaceModel(ABC):
    def __init__(self):
        self.localmodel=LocalLLM()
        self.init()
    
    
    @abstractmethod
    def init(self,**kwargs):
        pass
    
    @abstractmethod
    def forward(self, **kwargs):
        pass
    
    @abstractmethod
    def embedding(self,**kwargs):
        pass
        
    