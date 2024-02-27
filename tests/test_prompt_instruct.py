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
from ananke.prompt import Prompt

__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"


def test_prompt_pack():
    prompt = Prompt()

    instructed_init_prompt = """
    The below text is you need to process
    ```markdown
    {text}
    {extra_param}
    ```
    """

    instructed_forward_prompt = """
    The below data is you need process:
    ```
    Nodes:
    ```
    {nodes}
    ```
    Relationships:
    ```
    {relationships}
    ```
    questions or sentences:
    ```
    {user_input}
    """

    prompt.set_template(instructed_init_prompt, instructed_forward_prompt)

    init_formatted_prompt = prompt.init(text="Sample text to process", extra_param="Extra parameter")
    forward_formatted_prompt = prompt(nodes="Node data", relationships="Relationship data", user_input="User input")

    # print("Initialized Prompt:")
    # print(init_formatted_prompt)

    # print("\nForward Prompt:")
    # print(forward_formatted_prompt)