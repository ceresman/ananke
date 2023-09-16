# Copyright 2023 undefined
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ---------------------------------------------------------------------------- #
#                           FastAPI server definition                          #
# ---------------------------------------------------------------------------- #
from ananke.base import BaseServer
from fastapi import FastAPI


class Server(BaseServer):
    def __init__(self):
        super().__init__()
        self.name = "Server"
        self.logger.info(f"Initialized {self.name}.")
        self.app = FastAPI()

    def run(self):
        self.logger.info(f"Running {self.name}.")
        self.app.run()

    def stop(self):
        self.logger.info(f"Stopping {self.name}.")
        self.app.stop()