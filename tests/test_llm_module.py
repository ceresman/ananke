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
import pytest
from ananke.llm.thudm import ZhiPuModel
from ananke.llm.azure import AzureOpenAI
from ananke.llm.ernie import ErnieModel
__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"


# TODO Module init & Add to Flow & Process
def test_zhipu_model():
    pass
    # ernie_bot = ErnieModel()

    # Chat completion example
    # chat_messages = [
    #     {'role': 'user', 'content': "hi"}
    # ]
    # chat_result = ernie_bot.chat(model='ernie-bot-4', messages=chat_messages)
    # ernie_bot.logger.info(chat_result)

    # Text embedding example
    # embedding_input = [
    #     "hi"
    # ]
    # embedding_result = ernie_bot.embedding(model='ernie-text-embedding', input_text=embedding_input)
    # ernie_bot.logger.info(embedding_result)

    
    # pass
    # zp_model=ZhiPuModel()
    # print(zp_model.invoke("Hi"))
    # openai_model=AzureOpenAI()
    # print(openai_model.chat("Hi"))
    