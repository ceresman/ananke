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

import yaml
from pprint import pprint


class YAMLCONFIG():
    def __init__(self,**kwargs):
        super().__init__()
        # from template
        # self.config_template = YAML_CONFIG_TEMPLATE
        # from yaml file
        # self.config_file = kwargs.get("config_file",None)
        # self.default_config_file="./src/ananke/base/config.yaml"
        self.default_config_file="/workspace/huangyongfeng/ananke/src/ananke/base/config.yaml"

        if kwargs.get("config_file",None) is None:
            self.config_file=self.default_config_file
        else:
            self.config_file=kwargs.get("config_file",None)
        with open(self.config_file, 'r') as file:
            self.config = yaml.safe_load(file)
            # pprint(self.config, width=30)

        
    def __call__(self):
        return self.config
