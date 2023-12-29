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
from ananke.data.general  import Paper
from pdfquery import PDFQuery

__author__ = "OOXXXXOO"
__copyright__ = "OOXXXXOO"
__license__ = "MIT"

def test_paper():
    path = "example/data/gpt3.pdf"
    # config = YAMLCONFIG()
    paper = Paper()
    data = paper.read(path)
    print(data)

test_paper()


