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


from typing import Any
from ananke.base import BasePrompt
from ananke.prompt.prompt_collection import KG_SENTENCES_RELATED_INIT,KG_SENTENCES_RELATED_FORWARD
import re

class Prompt(BasePrompt):
    """
    A class for generating prompts using templates.

    This class allows you to create prompts by defining templates with placeholders, which are then filled with values
    specified as keyword arguments. It provides methods for initializing and forwarding prompts using different templates.

    :param init_template: The template for the initialization prompt.
    :param forward_template: The template for the forward prompt.
    """

    def __init__(self, init_template=None, forward_template=None):
        """
        Initialize a Prompt instance with optional initialization and forward templates.

        :param init_template: The template for the initialization prompt.
        :param forward_template: The template for the forward prompt.
        """
        super().__init__(name="Prompt")
        self.init_prompt_template = None
        self.forward_prompt_template = None
        self.set_template(init_template, forward_template)

    def set_template(self, init_template, forward_template):
        """
        Set the initialization and forward prompt templates.

        :param init_template: The template for the initialization prompt.
        :param forward_template: The template for the forward prompt.
        """
        self.init_prompt_template = init_template
        self.forward_prompt_template = forward_template

    def validate_parameters(self, template, **kwargs):
        """
        Validate that the provided keyword arguments match the placeholders in the template.

        :param template: The template with placeholders.
        :param kwargs: Keyword arguments to be filled in the template.
        :raises ValueError: If the keys in the template do not match the provided keyword arguments.
        """
        self.template_keys = set(re.findall(r'{(.*?)}', template))
        self.logger.debug(f"Template keys: {self.template_keys}")
        self.provided_keys = set(kwargs.keys())
        self.logger.debug(f"Provided keys: {self.provided_keys}")
        if self.template_keys != self.provided_keys:
            raise ValueError(f"Parameter mismatch. Expected keys: {self.template_keys}, Provided keys: {self.provided_keys}")

    def format_prompt(self, template, **kwargs):
        """
        Format the prompt by filling in the placeholders with values from keyword arguments.

        :param template: The template with placeholders.
        :param kwargs: Keyword arguments to be filled in the template.
        :return: The formatted prompt.
        :raises ValueError: If the template is not set.
        """
        self.validate_parameters(template, **kwargs)
        if template is None:
            raise ValueError("Template is not set. Please set the template before formatting.")
        return template.format(**kwargs)

    def init(self, **kwargs):
        """
        Generate an initialization prompt based on the provided template and keyword arguments.

        :param kwargs: Keyword arguments to be filled in the initialization template.
        :return: The formatted initialization prompt.
        :raises ValueError: If the initialization template is not set.
        """
        if self.init_prompt_template is None:
            raise ValueError("Init prompt template is not set. Please set the init prompt template before using.")
        return self.format_prompt(self.init_prompt_template, **kwargs)

    def forward(self, **kwargs):
        """
        Generate a forward prompt based on the provided template and keyword arguments.

        :param kwargs: Keyword arguments to be filled in the forward template.
        :return: The formatted forward prompt.
        :raises ValueError: If the forward prompt template is not set.
        """
        if self.forward_prompt_template is None:
            raise ValueError("Forward prompt template is not set. Please set the forward prompt template before using.")
        return self.format_prompt(self.forward_prompt_template, **kwargs)

    def __call__(self, **kwargs):
        """
        Call the 'forward' method to generate a forward prompt using provided keyword arguments.

        :param kwargs: Keyword arguments to be filled in the forward template.
        :return: The formatted forward prompt.
        """
        return self.forward(**kwargs)
