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

from ananke.module import Module
from ananke.data import StructuredChunk


class GraphExtractor(Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, input_data: StructuredChunk):
        self.logger.debug(f"GraphExtractor: {input_data}")
        self.threading_info()
        pass

    def __call__(self, input_data: StructuredChunk):
        return self.forward(input_data)

    def __repr__(self):
        return "GraphExtractor"


class LogicalRepresentationExtractor(Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, input_data: StructuredChunk):
        self.logger.debug(f"LogicalRepresentationExtractor: {input_data}")
        self.threading_info()
        pass

    def __call__(self, input_data: StructuredChunk):
        return self.forward(input_data)

    def __repr__(self):
        return "LogicalRepresentationExtractor"


class MathRepresentationExtractor(Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, input_data: StructuredChunk):
        self.logger.debug(f"MathRepresentationExtractor: {input_data}")
        self.threading_info()
        pass

    def __call__(self, input_data: StructuredChunk):
        return self.forward(input_data)

    def __repr__(self):
        return "MathRepresentationExtractor"


class VectorEmbeddingExtractor(Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, input_data: StructuredChunk):
        self.logger.debug(f"VectorEmbeddingExtractor: {input_data}")
        self.threading_info()
        pass

    def __call__(self, input_data: StructuredChunk):
        return self.forward(input_data)

    def __repr__(self):
        return "VectorEmbeddingExtractor"


class UserIntentExtractor(Module):
    def __init__(self):
        super().__init__()
        pass

    def forward(self, input_data: StructuredChunk):
        self.logger.debug(f"UserIntentExtractor: {input_data}")
        self.threading_info()
        pass

    def __call__(self, input_data: StructuredChunk):
        return self.forward(input_data)

    def __repr__(self):
        return "UserIntentExtractor"
