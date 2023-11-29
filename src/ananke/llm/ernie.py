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

import erniebot
from ananke.llm import RemoteLLM

class ErnieModel(RemoteLLM):
    def __init__(self, api_type='aistudio', access_token=None):
        super(ErnieModel, self).__init__()
        erniebot.api_type = api_type
        erniebot.access_token = access_token

    def chat(self, model, messages):
        response = erniebot.ChatCompletion.create(model=model, messages=messages)
        return response.get_result()

    def embedding(self, model, input_text):
        response = erniebot.Embedding.create(model=model, input=input_text)
        return response.get_result()