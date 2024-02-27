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
import zhipuai
import json

import zhipuai

class ZhiPuModel(RemoteLLM):
    def __init__(self, api_key=None):
        super().__init__()
        self.logger.debug(self.config.config["ZHIPU"][0]["KEY"])
        zhipuai.api_key = self.config.config["ZHIPU"][0]["KEY"]
        self.conversation_history = []

    def update_history(self, role, content):
        self.conversation_history.append({"role": role, "content": content})

    def invoke(self, prompt, top_p=0.7, temperature=0.9):
        response = zhipuai.model_api.invoke(
            model="chatglm_turbo",
            prompt=[{"role": "user", "content": prompt}],
            top_p=top_p,
            temperature=temperature,
        )
        self.update_history("user", prompt)
        return response

    def async_invoke(self, prompt, top_p=0.7, temperature=0.9):
        response = zhipuai.model_api.async_invoke(
            model="chatglm_turbo",
            prompt=[{"role": "user", "content": prompt}],
            top_p=top_p,
            temperature=temperature,
        )
        self.update_history("user", prompt)
        return response

    def sse_invoke(self, prompt, top_p=0.7, temperature=0.9):
        response = zhipuai.model_api.sse_invoke(
            model="chatglm_turbo",
            prompt=[{"role": "user", "content": prompt}],
            top_p=top_p,
            temperature=temperature,
        )

        for event in response.events():
            if event.event == "add":
                self.update_history("bot", event.data)
            elif event.event == "error" or event.event == "interrupted":
                print(event.data)
            elif event.event == "finish":
                self.update_history("bot", event.data)
                print(event.meta)
            else:
                print(event.data)

    def query_async_invoke_result(self, task_id):
        response = zhipuai.model_api.query_async_invoke_result(task_id, api_key=self.api_key)
        return response
# # Example usage:
# api_key = "your_api_key"
# zhipuai_wrapper = ZhipuaiModelWrapper(api_key)

# prompt = "你能自我介绍一下吗"
# # invoke_response = zhipuai_wrapper.invoke(prompt)
# # async_invoke_response = zhipuai_wrapper.async_invoke(prompt)
# sse_invoke_response = zhipuai_wrapper.sse_invoke(prompt)
# # query_result_response = zhipuai_wrapper.query_async_invoke_result("your_task_id")

# print("Invoke Response:", invoke_response)
# print("Async Invoke Response:", async_invoke_response)
# print("SSE Invoke Response:", sse_invoke_response)
# print("Query Result Response:", query_result_response)
