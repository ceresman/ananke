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
from ananke.llm import RemoteLLM
from zhipuai import ZhipuAI


class ZhiPu(RemoteLLM):
    def __init__(self,model="glm-4", api_key=None):
        super().__init__()
        if api_key is None:
            self.api_key=self.config()["ZHIPU"]["KEY"]
            self.model=self.config()["ZHIPU"]["MODEL"]
        else:
            self.api_key=api_key
            self.model=model
        self.client = ZhipuAI(api_key=self.api_key)
        self.history = [
             {"role": "system", "content": "你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。"}
        ]

    def chat(self, messages):
        self.history.append(
            {"role": "user", "content":messages}
        )
        response = self.client.chat.completions.create(
            model=self.model, messages=self.history
        )
        self.history.append(
            {"role": "system", "content":response.choices[0].message}
        )
        return response.choices[0].message

    def stream_chat(self, messages):
        self.history.append(
            {"role": "user", "content":messages}
        )
        response = self.client.chat.completions.create(
            model=self.model, messages=self.history, stream=True
        )

        for chunk in response:
            yield chunk.choices[0].delta
        self.history.append(
            {"role": "system", "content":response.choices[0].message}
        )