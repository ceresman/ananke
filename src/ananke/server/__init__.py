# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Winshare Tom <tanwenxuan@live.com>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/14 17:03:07 by Winshare To       #+#    #+#              #
#    Updated: 2023/12/14 17:03:28 by Winshare To      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


from ananke.base import BaseServer
from fastapi import FastAPI


class Server(BaseServer):
    # TODO : Implement Server Class for ananke dataframwork
    def __init__(self,**kwargs):
        super().__init__()
        self.type = "Server"
        self.logger.info(f"Initialized {self.type}.")
        self.app = FastAPI()

    def run(self):
        self.logger.info(f"Running {self.type}.")
        self.app.run()

    def stop(self):
        self.logger.info(f"Stopping {self.type}.")
        self.app.stop()